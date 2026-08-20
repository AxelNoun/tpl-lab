"""Chantier 2 — the bridge law, as code rather than a metaphor.

A geometric claim about neural data is empty until each geometric element names
an observable, a unit, and a script. This module is that script for the only
element that currently has one: a point of the hypothesized manifold is a
population spike-count vector. It does not invent a mapping to R^7. Reducing
the recordings to 7 principal components is the degree of freedom docs/02
exists to forbid: it would cap the ambient dimension at 7 and so manufacture
the prediction.

What this module refuses, on purpose:
- PCA / NMF / any learned projection to 7 (or 8) dimensions
- per-channel z-scoring or square-root transforms (both change TwoNN, which
  is not invariant to anisotropic rescaling)
- pooling several cortical areas into one cloud
- a firing-rate threshold beyond 'at least one spike' (rate cuts are a classic
  HARKing knob)

`--data` for run_id is already-binned counts; `bin_population` is the only
supported path from events to those counts.
"""
import warnings

import numpy as np

MIN_CHANNELS = 7  # S^6 ⊂ R^7; fewer coordinates cannot host the manifold
WINDOW_MS = 50


def bin_population(times, unit_ids, t_start, t_stop, window_ms=WINDOW_MS):
    """Non-overlapping spike-count windows. Returns (n_windows, n_units).

    `times` in seconds, `unit_ids` any hashable labels. Units that never spike
    in [t_start, t_stop) still occupy a column of zeros; `prepare_population`
    drops those, and nothing else.
    """
    if window_ms != WINDOW_MS:
        raise ValueError(f"window_ms is frozen at {WINDOW_MS} by the prereg; "
                         f"got {window_ms}")
    times = np.asarray(times, dtype=float)
    unit_ids = np.asarray(unit_ids)
    if times.shape != unit_ids.shape:
        raise ValueError("times and unit_ids must have the same length")
    units, inv = np.unique(unit_ids, return_inverse=True)
    t0_ms = int(round(t_start * 1000))
    t1_ms = int(round(t_stop * 1000))
    n_win = (t1_ms - t0_ms) // window_ms
    if n_win < 1:
        raise ValueError("interval shorter than one window")
    idx = np.floor((times * 1000 - t0_ms) / window_ms).astype(int)
    ok = (idx >= 0) & (idx < n_win)
    X = np.zeros((n_win, len(units)), dtype=float)
    np.add.at(X, (idx[ok], inv[ok]), 1.0)
    return X, units


def prepare_population(X, min_channels=MIN_CHANNELS):
    """Validate a (n_windows, n_channels) array and drop silent units.

    This is the last step before `run_id`. It never reduces rank, never
    rescales axes, never interpolates. The returned cloud lives in R^N with
    N = number of units that fired at least once.
    """
    X = np.asarray(X, dtype=float)
    if X.ndim != 2:
        raise ValueError(f"population vectors must be 2-D (n_windows, n_channels); "
                         f"got shape {X.shape}")
    silent = np.all(X == 0, axis=0)
    n_silent = int(silent.sum())
    if n_silent:
        warnings.warn(
            f"prepare_population: dropping {n_silent} units that never spiked "
            f"(not a rate threshold — they contribute a degenerate axis)",
            RuntimeWarning,
            stacklevel=2,
        )
        X = X[:, ~silent]
    n_channels = X.shape[1]
    if n_channels < min_channels:
        raise ValueError(
            f"{n_channels} active channels < {min_channels} : S^6 cannot sit in "
            f"R^{n_channels}. Record more units; do not pad or PCA-up."
        )
    return X


def refuse_reduction(X, claimed_coords=None):
    """Guard for the spectral test: coordinates must ALREADY be 7-D.

    The project will not compute those coordinates from N-channel recordings.
    Linear mixing (the realistic observation model, `s6_flow.observe`) destroys
    the O(7) spectrum, so inventing a 7-D basis to recover it would be
    fitting the prediction to the data.
    """
    X = np.asarray(X, dtype=float)
    n = X.shape[1] if claimed_coords is None else int(claimed_coords)
    if n != 7:
        raise ValueError(
            f"spectral predictions A/B are statements about S^6 ⊂ R^7; "
            f"ambient dim is {n}. PCA to 7 is forbidden (docs/02). "
            f"This test is not applicable to mixed N-channel recordings."
        )
    return X
