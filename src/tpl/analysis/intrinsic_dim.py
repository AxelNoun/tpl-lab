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
