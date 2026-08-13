"""Upgrade #3 — the primary real-data readout: state CONTRAST, not absolutes.

TPL predicts geometric structure collapses when consciousness does
(wake -> propofol/deep sleep). Benchmark to beat on shared datasets: PCI
(Casali et al. 2013). This module computes per-condition metrics and their
bootstrap contrast; loaders for real datasets plug into `metrics_for`.
"""
import numpy as np

from tpl.analysis.intrinsic_dim import twonn
from tpl.analysis.topology import betti1
from tpl.analysis.model_comparison import rank_candidates


def metrics_for(pts, seed=0):
    ranks = rank_candidates(pts, n_boot=2, seed=seed)
    best = next(iter(ranks))
    return {"id": twonn(pts), "b1": betti1(pts, seed=seed),
            "best_geometry": best, "score_S6": ranks.get("S6", np.nan)}


def contrast(pts_a, pts_b, n_boot=5, seed=0):
    """Metrics for two conditions + bootstrap CI on the ID difference."""
    rng = np.random.default_rng(seed)
    ma, mb = metrics_for(pts_a, seed), metrics_for(pts_b, seed)
    diffs = []
    for _ in range(n_boot):
        ia = rng.choice(len(pts_a), len(pts_a), replace=True)
        ib = rng.choice(len(pts_b), len(pts_b), replace=True)
        diffs.append(twonn(pts_a[ia]) - twonn(pts_b[ib]))
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return {"A": ma, "B": mb, "delta_id": float(np.mean(diffs)),
            "delta_id_ci95": (float(lo), float(hi))}
