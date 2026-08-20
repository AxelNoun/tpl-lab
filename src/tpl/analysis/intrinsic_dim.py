"""Chantier 6 — TwoNN intrinsic-dimension estimator.

Facco, d'Errico, Rodriguez & Laio (2017), Scientific Reports (open access):
uses only the ratio mu = r2/r1 of the two nearest-neighbour distances.
Under mild assumptions F(mu) = 1 - mu^(-d), so a zero-intercept regression of
-log(1-F) on log(mu) yields d. This gives the project its one *rigid* number.

Known limits, both measured (see docs/RESULTATS_NEGATIFS.md, audit v2):
- Temporally correlated input biases d DOWN; decorrelate before estimating
  (tests/test_dim.py keeps the pitfall visible).
- Estimates converge to the true d from BELOW: ~5.8 at n = 1000 for a true 6.
  Small n therefore risks a false refutation against a +/-0.5 tolerance.
"""
import warnings

import numpy as np
from scipy.spatial import cKDTree


def max_lag_for(n: int) -> int:
    """Cap on the search for a decorrelation lag. Callers compare against it to
    tell 'decorrelated at lag L' from 'never decorrelated'."""
    return max(1, min(n // 4, 1000))


def autocorrelation_time(traj, threshold: float = 0.1, max_lag: int | None = None) -> int:
    """Smallest lag at which the mean per-channel autocorrelation drops below
    `threshold`. This is the decimation factor the preregistration asks for.

    Averaged across channels: a population trajectory has one shared timescale,
    and per-channel thresholds would make the factor depend on which channel
    happens to be slowest.

    Returns `max_lag` when the series never decorrelates, and warns. That case
    is NOT a decimation factor and must not be treated as one: the samples that
    survive are still correlated, so TwoNN stays biased low on them. A chaotic
    RNN at g = 1.8 hit the cap and yielded a plausible-looking d = 6.14 on 140
    samples that were never independent (audit v2).
    """
    x = np.asarray(traj, dtype=float)
    if x.ndim == 1:
        x = x[:, None]
    cap = max_lag or max_lag_for(len(x))
    max_lag = cap
    x = x - x.mean(0)
    var = (x ** 2).mean(0)
    x = x[:, var > 0]
    if x.shape[1] == 0:
        return 1
    var = var[var > 0]
    for lag in range(1, max_lag + 1):
        if float(np.mean((x[:-lag] * x[lag:]).mean(0) / var)) < threshold:
            return lag
    warnings.warn(
        f"autocorrelation_time: never fell below {threshold} within {cap} lags; "
        f"the series is not decorrelatable at this length and the returned lag "
        f"is a cap, not a decimation factor",
        RuntimeWarning,
        stacklevel=2,
    )
    return cap


def decorrelate(traj, threshold: float = 0.1, max_lag: int | None = None):
    """Thin a trajectory to (approximately) independent samples.

    TwoNN assumes i.i.d. sampling; temporal correlation biases it DOWN, which is
    the direction that would manufacture a spurious 'd = 6'. The factor must
    therefore come from the data, never from the analyst: on a synthetic S6
    rotation of true dimension 6 (20000 steps), hand-picked factors 1, 2, 5 and
    10 give 4.05, 4.49, 5.40 and 6.01 — a range several times the +/- 0.5
    tolerance, so the choice alone decides the verdict.

    Thinning is not free, and the rule does NOT remove the problem: factors 50
    and 100 on that same trajectory give 5.19 and 5.08, back below tolerance,
    because only 400 and 200 samples survive and TwoNN is biased low at small n.
    Decorrelating and keeping enough samples pull in opposite directions, which
    is why the pipeline pairs this rule with a minimum n (see run_id).

    Returns (thinned, lag).
    """
    lag = autocorrelation_time(traj, threshold=threshold, max_lag=max_lag)
    return np.asarray(traj, dtype=float)[::lag], lag


def twonn(points: np.ndarray, discard: float = 0.1, dedupe: bool = True) -> float:
    """Estimate intrinsic dimension. Exact duplicate points are dropped by default.

    Duplicates violate the continuous-density assumption and inflate the
    estimate badly: a duplicated point has r1 = 0 and is discarded, while its
    neighbours see r2/r1 = 1 exactly, contributing nothing to the fit yet still
    consuming rank in the empirical CDF. On d = 6 data a with-replacement
    resample reads ~9 instead of ~6. Duplicates appear whenever one resamples
    with replacement, and in real recordings whenever two windows are identical
    (all-zero spike counts, saturated channels). Removal is reported, never
    silent.
    """
    pts = np.asarray(points, dtype=float)
    if dedupe:
        uniq = np.unique(pts, axis=0)
        if len(uniq) < len(pts):
            warnings.warn(
                f"twonn: dropped {len(pts) - len(uniq)} exact duplicate point(s) "
                f"of {len(pts)}; they break the k-NN ratio statistic",
                RuntimeWarning,
                stacklevel=2,
            )
            pts = uniq
    tree = cKDTree(pts)
    d, _ = tree.query(pts, k=3)  # self, nn1, nn2
    r1, r2 = d[:, 1], d[:, 2]
    ok = r1 > 0
    mu = np.sort(r2[ok] / r1[ok])
    n = mu.size
    keep = int(np.floor(n * (1 - discard)))
    mu = mu[:keep]
    F = np.arange(1, keep + 1) / n
    x = np.log(mu)
    y = -np.log(1.0 - F)
    return float((x @ y) / (x @ x))
