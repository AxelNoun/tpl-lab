"""Chantier 6 — TwoNN intrinsic-dimension estimator.

Facco, d'Errico, Rodriguez & Laio (2017), Scientific Reports (open access):
uses only the ratio mu = r2/r1 of the two nearest-neighbour distances.
Under mild assumptions F(mu) = 1 - mu^(-d), so a zero-intercept regression of
-log(1-F) on log(mu) yields d. This gives the project its one *rigid* number.
"""
import numpy as np
from scipy.spatial import cKDTree


def twonn(points: np.ndarray, discard: float = 0.1) -> float:
    pts = np.asarray(points, dtype=float)
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
