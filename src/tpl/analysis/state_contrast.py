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
from tpl.analysis.model_comparison import select_geometry


def metrics_for(pts, seed=0):
    """`best_geometry` is None when NO candidate actually fits — the collapse
    TPL predicts under anaesthesia should show up exactly that way, rather than
    as a winner named by default."""
    sel = select_geometry(pts, seed=seed, n_boot=2)
    return {"id": twonn(pts), "b1": betti1(pts, seed=seed),
            "best_geometry": sel["geometry"],
            "best_candidate": sel["best_candidate"],
            "fit_score": sel["score"],
            "score_S6": sel["ranking"].get("S6", np.nan)}


def contrast(pts_a, pts_b, n_boot=1000, frac=0.632, seed=0):
    """Metrics for two conditions + a subsampling CI on the ID difference.

    Resampling WITH replacement is invalid for a k-NN estimator: the duplicates
    it creates read as d ~ 9 on d = 6 data (audit v2, docs/RESULTATS_NEGATIFS.md).
    The interval therefore comes from m-out-of-n subsampling WITHOUT replacement,
    m = frac * n.

    The raw percentiles of those subsample differences are kept, deliberately,
    after the textbook alternative was tried and measured
    (`python -m tpl.analysis.calibration --ci-coverage`). Rescaling the root
    theta_m - theta_n by sqrt(m/n) (Politis & Romano 1994) is the principled fix
    for an interval computed at m < n, and it makes coverage WORSE: 65% instead
    of 98% on a 6-vs-3 contrast. TwoNN's bias barely moves between m and n, so
    subsampling cannot see it, let alone correct it, and the rescaling removes
    the surplus width that was the only thing compensating for it.

    THIS INTERVAL IS A DETECTION TEST, NOT AN EFFECT SIZE. Coverage of a known
    true difference is 98% for a 6-vs-3 contrast but only 40% for 10-vs-3: at
    high d, TwoNN's bias (~1.3 on the difference) dwarfs the interval width
    (~1.5) and no resampling scheme can repair it, because resampling has no
    access to bias. What survives is the sign: the bias grows with d, so the
    difference is UNDERestimated and the interval is pulled towards zero. The
    prereg's 'CI95 excluding 0' therefore stays conservative — the claim gets
    harder, never easier — but the width must never be reported as an error bar.

    Related artefact, same cause: the interval can sit off-centre from
    `delta_id` and even exclude it (-2.27 for [-2.18, -1.30] on the run_id
    dry-run) when the two conditions differ a lot in dimension.
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
    theta = float(ma["id"] - mb["id"])
    ma_sub, mb_sub = int(len(pts_a) * frac), int(len(pts_b) * frac)
    diffs = np.empty(n_boot)
    for k in range(n_boot):
        ia = rng.choice(len(pts_a), ma_sub, replace=False)
        ib = rng.choice(len(pts_b), mb_sub, replace=False)
        diffs[k] = twonn(pts_a[ia]) - twonn(pts_b[ib])
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    return {"A": ma, "B": mb,
            "delta_id": theta,
            "delta_id_ci95": (float(lo), float(hi)),
            "delta_id_subsample_mean": float(diffs.mean()),
            "n_boot": n_boot, "subsample_frac": frac}
