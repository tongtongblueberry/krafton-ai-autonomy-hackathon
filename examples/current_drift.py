"""Separate a constant velocity offset from a position residual.

Inputs to position_residual_with_current must be finite: two same-shape arrays
(episodes, times, 2), sharing their starting position, and a nonzero time vector
in seconds since start. Positions are in metres. A fitted offset is in m/s.
"""


from __future__ import annotations


import numpy as np


def position_residual_with_current(predicted, observed, times):
    """Project only a constant episode current out of world-position residuals.

    A velocity measurement residual remains in the objective, so a constant
    body-speed error cannot be made free merely by this nuisance projection.
    The fitted current is never passed to the deployed simulator.
    """
    delta = np.asarray(observed)-np.asarray(predicted)
    times = np.asarray(times)
    if delta.ndim != 3 or delta.shape[-1] != 2 or times.shape != (delta.shape[1],):
        raise ValueError("expected episode/time/two-coordinate position arrays")
    current = np.einsum("t,etd->ed", times, delta)/np.dot(times, times)
    return -delta+times[None, :, None]*current[:, None, :], current


def test_nuisance_current_projection_removes_only_constant_world_drift():
    times = np.arange(1, 41)*.1
    predicted = np.random.default_rng(5).normal(size=(3, 40, 2))
    known = np.array([[.03, -.02], [-.01, .04], [.05, .01]])
    observed = predicted+times[None, :, None]*known[:, None, :]
    residual, current = position_residual_with_current(predicted, observed, times)
    np.testing.assert_allclose(current, known, atol=1e-14)
    np.testing.assert_allclose(residual, 0., atol=1e-14)
    curved = observed.copy()
    curved[0, :, 0] += np.sin(times)
    residual, _ = position_residual_with_current(predicted, curved, times)
    assert np.max(np.abs(residual[0])) > .1


if __name__ == "__main__":
    test_nuisance_current_projection_removes_only_constant_world_drift()
    print("Constant drift: recovered all three known offsets (m/s).")
    print("Curved perturbation: the maximum remaining position error exceeds 0.1 m.")
