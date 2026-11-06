"""Evaluation helpers used in the robomimic Lift comparison.

Supply one record per seed and policy. The caller is responsible for providing
unique seeds and a planned count covering all attempts.
"""

from __future__ import annotations

import math


def wilson_interval(successes: int, completed: int) -> list[float] | None:
    if not 0 <= successes <= completed:
        raise ValueError("invalid success denominator")
    if completed == 0:
        return None
    z = 1.959963984540054
    rate = successes / completed
    divisor = 1 + z * z / completed
    centre = (rate + z * z / (2 * completed)) / divisor
    radius = z * math.sqrt(rate * (1 - rate) / completed + z * z / (4 * completed**2)) / divisor
    return [max(0., centre - radius), min(1., centre + radius)]


def summarize_episodes(label: str, planned: int, episodes: list[dict], seconds: float) -> dict:
    completed = [e for e in episodes if e["termination"] not in ("exception", "wall_censored")]
    successes = sum(bool(e["success"]) for e in completed)
    return {"label": label, "planned": planned, "attempted": len(episodes),
            "completed": len(completed), "unattempted": planned - len(episodes),
            "successes": successes, "exceptions": sum(e["termination"] == "exception" for e in episodes),
            "censored": sum(e["termination"] == "wall_censored" for e in episodes),
            "horizon_failures": sum(e["termination"] == "horizon" for e in episodes),
            "success_rate_completed": successes / len(completed) if completed else None,
            "wilson95_completed": wilson_interval(successes, len(completed)),
            "planned_success_bounds": [successes / planned, (successes + planned - len(completed)) / planned],
            "mean_return_completed": math.fsum(e["return"] for e in completed) / len(completed) if completed else None,
            "mean_length_completed": math.fsum(e["length"] for e in completed) / len(completed) if completed else None,
            "seconds": seconds, "episodes": episodes}


def paired_success(learned: list[dict], public: list[dict], planned: int) -> dict:
    complete = lambda rows: {e["seed"]: e for e in rows if e["termination"] not in ("exception", "wall_censored")}
    left, right = complete(learned), complete(public)
    seeds = sorted(set(left) & set(right))
    cells = {"both_success": 0, "learned_only": 0, "public_only": 0, "both_failure": 0}
    for seed in seeds:
        a, b = left[seed], right[seed]
        if a["initial_state_sha256"] != b["initial_state_sha256"] or a["initial_observation_sha256"] != b["initial_observation_sha256"]:
            raise ValueError("paired episode initial identity mismatch")
        key = ("both_success" if b["success"] else "learned_only") if a["success"] else ("public_only" if b["success"] else "both_failure")
        cells[key] += 1
    return {"planned": planned, "completed_pairs": len(seeds), "incomplete_pairs": planned - len(seeds),
            "cells": cells, "learned_minus_public_rate": (cells["learned_only"] - cells["public_only"]) / len(seeds) if seeds else None,
            "episode_seed_ids": seeds, "training_seed_uncertainty": "not estimated; one training seed"}
