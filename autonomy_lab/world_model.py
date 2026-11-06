"""Finite-history, action-conditioned GRU; no state outside the graph ctx."""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F


class RecurrentLatentDynamics(nn.Module):
    def __init__(self, layout, hidden_size: int = 128):
        super().__init__()
        self.layout = layout
        c = layout.channels
        self.project = nn.Sequential(
            nn.Conv2d(c, 16, 3, stride=2, padding=1), nn.SiLU(), nn.Flatten(),
            nn.Linear(16 * ((layout.grid + 1) // 2) ** 2, 64), nn.SiLU(),
        )
        self.cell = nn.GRUCell(66, hidden_size)
        self.hidden_size = hidden_size
        self.condition = nn.Sequential(nn.Linear(c + hidden_size + 1, 32), nn.SiLU(),
                                       nn.Linear(32, 32))
        self.in_conv = nn.Conv2d(c, 32, 3, padding=1)
        self.mid_conv = nn.Conv2d(32, 32, 3, padding=1)
        self.out_conv = nn.Conv2d(32, c, 1)

    def forward(self, history, action, context_actions=None):
        if context_actions is None:
            raise ValueError("GRU requires the actions between retained frames")
        batch, steps = history.shape[:2]
        features = self.project(history.reshape(-1, *history.shape[2:])).reshape(batch, steps, 64)
        hidden = features[:, 0].new_zeros((batch, self.hidden_size))
        zero = features[:, 0, :1] * 0.0
        # The fixed trip count exports as standard gate ops, not a dynamic loop.
        for t in range(self.layout.context_length):
            previous = zero if t == 0 else context_actions[:, t - 1:t]
            valid = zero if t == 0 else zero + 1.0
            hidden = self.cell(torch.cat((features[:, t], previous, valid), 1), hidden)
        latest = history[:, -1]
        condition = self.condition(torch.cat((latest.mean((2, 3)), hidden,
                                               action.reshape(batch, 1)), 1))
        h = F.silu(self.in_conv(latest) + condition[:, :, None, None])
        h = F.silu(self.mid_conv(h))
        return torch.clamp(latest + 0.1 * torch.tanh(self.out_conv(h)), -1.0, 1.0)
