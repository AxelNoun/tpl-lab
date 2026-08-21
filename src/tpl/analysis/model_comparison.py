"""Upgrade #2 — which candidate geometry best matches the data?

Pragmatic, honest first pass: a 'shape fingerprint' per candidate =
(a) intrinsic dimension (TwoNN), (b) the pairwise-distance distribution
(Osada et al.'s shape distribution, scale-normalized), (c) top H1 persistences.
Score = weighted 1D-Wasserstein / absolute differences, bootstrapped over
candidate resamples. This is model *ranking*, not posterior probability.
TODO: a variational mGPLVM (Jensen et al. 2020) would still be an optional
pytorch extra. The numpy geodesic-GP in `tpl.analysis.manifold_evidence`
is SECONDARY: it does not replace `select_geometry` and does not retune
MAX_FIT_SCORE. It also does not recover T6 (docs/22).
"""

import numpy as np

from tpl.analysis.intrinsic_dim import twonn
from tpl.analysis.topology import h1_persistences, rescale_to_unit
from tpl.generative.manifolds import CANDIDATES


def _pairwise_hist(pts, bins=40, n_max=800, seed=0):
    rng = np.random.default_rng(seed)
    if len(pts) > n_max:
        pts = pts[rng.choice(len(pts), n_max, replace=False)]
    d = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=-1)
    d = d[np.triu_indices_from(d, k=1)]
    d = d / np.median(d)  # scale-free
    h, _ = np.histogram(d, bins=bins, range=(0, 3), density=True)
    return h / h.sum()


def _wass1(p, q):
    return float(np.abs(np.cumsum(p) - np.cumsum(q)).sum())


def fingerprint(pts, seed=0):
    """Scale-invariant shape descriptor.

    The cloud is rescaled to mean radius 1 first. TwoNN and the median-normalised
    distance histogram are already scale-free, but H1 persistence lengths are not:
    without this, doubling the units of the same data scored 5.0 against itself
    instead of 0, and the R6 candidate (mean |x| = 0.86) was compared against
    S6/T6 (mean |x| = 1.0) partly on scale rather than on shape.
    """
    pts = rescale_to_unit(np.asarray(pts, float))
    return {
        "id": twonn(pts),
        "hist": _pairwise_hist(pts, seed=seed),
        "h1": h1_persistences(pts, n_landmarks=300, seed=seed)[:10],
    }


def _score(fa, fb):
    h1a = np.pad(fa["h1"], (0, max(0, 10 - len(fa["h1"]))))[:10]
    h1b = np.pad(fb["h1"], (0, max(0, 10 - len(fb["h1"]))))[:10]
    return (
        abs(fa["id"] - fb["id"])
        + 10.0 * _wass1(fa["hist"], fb["hist"])
        + 2.0 * float(np.abs(h1a - h1b).sum())
    )


def rank_candidates(data, n_boot=3, seed=0, candidates=None):
    """Return {name: mean score} — LOWER is better. Sorted dict.

    A RANKING only: it always names a winner. Use `select_geometry` when the
    honest answer may be 'none of these'.
    """
    candidates = candidates or CANDIDATES
    fd = fingerprint(np.asarray(data, float), seed=seed)
    out = {}
    for name, gen in candidates.items():
        s = [
            _score(
                fd, fingerprint(gen(n=2000, noise=0.02, seed=seed + 7 * b), seed=seed)
            )
            for b in range(n_boot)
        ]
        out[name] = float(np.mean(s))
    return dict(sorted(out.items(), key=lambda kv: kv[1]))


# Absolute goodness-of-fit cutoff, calibrated on synthetic data BEFORE any real
# data (CLAUDE.md R2) and frozen. Reproduce with:
#     python -m tpl.analysis.calibration --fit-threshold
# Measured at n = 2000, 4 seeds per cell:
#   true candidate geometry, noise <= 0.10, uniform OR not : 0.26 .. 2.43
#   none of the candidates (S3, S10, T3, 20-D gaussian)     : 4.05 .. 14.60
#   Kuramoto null of the project (K = 0 and K = 2)          : 4.20 .. 58.05
# 3.0 sits mid-margin and errs towards rejecting, like betti1's gap rule.
# DECLARED LIMIT: a genuine S6 carrying noise >= ~0.15 also scores above 3.0
# (3.34 at 0.15, 4.63 at 0.20) and is rejected. Beyond that noise level the
# test has no power rather than being wrong — see docs/09 and docs/12.
MAX_FIT_SCORE = 3.0


def select_geometry(data, seed=0, candidates=None, max_score=MAX_FIT_SCORE, n_boot=3):
    """Rank the candidates, then accept the winner only if it actually fits.

    `rank_candidates` on its own cannot say 'none of these': S^3 data comes out
    R6 and 20-D gaussian noise comes out T6, so a bare 'S6 won' carries a 1-in-3
    base rate. Returns `geometry=None` when no candidate clears `max_score`.
    """
    ranking = rank_candidates(data, n_boot=n_boot, seed=seed, candidates=candidates)
    best = next(iter(ranking))
    accepted = ranking[best] <= max_score
    return {
        "geometry": best if accepted else None,
        "best_candidate": best,
        "score": ranking[best],
        "accepted": accepted,
        "max_score": max_score,
        "ranking": ranking,
    }
