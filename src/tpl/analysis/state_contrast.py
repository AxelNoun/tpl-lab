"""Upgrade #3 — the primary real-data readout: state CONTRAST, not absolutes.

TPL predicts geometric structure collapses when consciousness does
(wake -> propofol/deep sleep). Benchmark to beat on shared datasets: PCI
(Casali et al. 2013). This module computes per-condition metrics and their
subsampled contrast; loaders for real datasets plug into `metrics_for`.
"""
import warnings

import numpy as np

from tpl.analysis.intrinsic_dim import twonn
from tpl.analysis.topology import betti1
from tpl.analysis.model_comparison import rank_candidates


def metrics_for(pts, seed=0):
    ranks = rank_candidates(pts, n_boot=2, seed=seed)
    best = next(iter(ranks))
    return {"id": twonn(pts), "b1": betti1(pts, seed=seed),
            "best_geometry": best, "score_S6": ranks.get("S6", np.nan)}


def contrast(pts_a, pts_b, n_boot=1000, frac=0.632, seed=0):
    """Metrics for two conditions + a subsampling CI on the ID difference.

    Resampling WITH replacement is invalid for a k-NN estimator: the duplicates
    it creates read as d ~ 9 on d = 6 data (audit v2, docs/RESULTATS_NEGATIFS.md).
    The interval therefore comes from m-out-of-n subsampling WITHOUT replacement,
    m = frac * n. Two consequences are declared rather than hidden: the interval
    is computed at m < n so it is CONSERVATIVE (wider than the interval at full
    n), and it is NOT recentred on the point estimate. `delta_id` is the
    full-sample difference, not the mean of the resamples.
    """
    if n_boot < 200:
        warnings.warn(
            f"contrast: n_boot={n_boot} is too small for a 95% percentile "
            f"interval (the 2.5/97.5 percentiles of a handful of draws are just "
            f"their min and max); use >= 1000 for anything reportable",
            RuntimeWarning,
            stacklevel=2,
        )
    rng = np.random.default_rng(seed)
    ma, mb = metrics_for(pts_a, seed), metrics_for(pts_b, seed)
    ma_sub, mb_sub = int(len(pts_a) * frac), int(len(pts_b) * frac)
    diffs = np.empty(n_boot)
    for k in range(n_boot):
        ia = rng.choice(len(pts_a), ma_sub, replace=False)
        ib = rng.choice(len(pts_b), mb_sub, replace=False)
        diffs[k] = twonn(pts_a[ia]) - twonn(pts_b[ib])
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return {"A": ma, "B": mb,
            "delta_id": float(ma["id"] - mb["id"]),
            "delta_id_ci95": (float(lo), float(hi)),
            "delta_id_subsample_mean": float(diffs.mean()),
            "n_boot": n_boot, "subsample_frac": frac}
