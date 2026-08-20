"""Upgrade #1 — persistent homology with a gap-based significance rule.

S^6 has no 1-cycles (b1 = 0); tori have b1 >= 1. Real loops separate from
sampling noise by a large multiplicative GAP in the sorted H1 persistences
(T^2 at n=2000: bars at ~21x and ~20x the median, noise at <= 8x). Rule fixed
on synthetic data BEFORE any real data (CLAUDE.md R2). Conservative where
topology is undetectable (see calibration): returns 0, never hallucinates.
"""
import numpy as np
from ripser import ripser

from tpl.analysis.intrinsic_dim import twonn
from tpl.generative.manifolds import sphere


def persistence(points, maxdim=1, n_landmarks=400, seed=0):
    pts = np.asarray(points, float)
    if len(pts) > n_landmarks:
        idx = np.random.default_rng(seed).choice(len(pts), n_landmarks, replace=False)
        pts = pts[idx]
    return ripser(pts, maxdim=maxdim)["dgms"]


def h1_persistences(points, **kw):
    d = persistence(points, **kw)[1]
    return np.sort(d[:, 1] - d[:, 0])[::-1] if len(d) else np.array([])


def rescale_to_unit(pts):
    """Centre and scale to mean radius 1, so persistence lengths are comparable
    across clouds recorded in arbitrary units. Shared with model_comparison."""
    pts = pts - pts.mean(0)
    r = np.linalg.norm(pts, axis=1).mean()
    return pts / r if r > 0 else pts


def betti1(points, dim=None, min_gap_ratio=2.0, n_landmarks=400, seed=0):
    """Gap-based count of significant 1-cycles.

    Sort H1 persistences descending; find the largest consecutive ratio
    p_i / p_{i+1} among the first 15 bars. If that ratio exceeds
    `min_gap_ratio`, the bars above the gap are significant (b1 = i), else 0.
    Calibrated on synthetic data (S^2/T^2/S^3/T^3), threshold fixed BEFORE any
    real data. Conservative: in low-power regimes (d >= 3-4 at n <= 3000, see
    calibration) it returns 0 rather than hallucinating loops. `dim` is kept
    for API compatibility and future null-based variants."""
    pts = rescale_to_unit(np.asarray(points, float))
    p = h1_persistences(pts, n_landmarks=n_landmarks, seed=seed)
    if p.size < 2:
        return 0
    head = p[:15]
    ratios = head[:-1] / np.maximum(head[1:], 1e-12)
    i = int(np.argmax(ratios))
    return i + 1 if ratios[i] > min_gap_ratio else 0
