"""Upgrade #2 — which candidate geometry best matches the data?

Pragmatic, honest first pass: a 'shape fingerprint' per candidate =
(a) intrinsic dimension (TwoNN), (b) the pairwise-distance distribution
(Osada et al.'s shape distribution, scale-normalized), (c) top H1 persistences.
Score = weighted 1D-Wasserstein / absolute differences, bootstrapped over
candidate resamples. This is model *ranking*, not posterior probability.
TODO (next step, documented): latent-variable manifold models with marginal
likelihood (mGPLVM, Jensen et al. 2020) — see docs/09-geometries-candidates.md.
"""
import numpy as np

from tpl.analysis.intrinsic_dim import twonn
from tpl.analysis.topology import h1_persistences
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
    return {
        "id": twonn(pts),
        "hist": _pairwise_hist(pts, seed=seed),
        "h1": h1_persistences(pts, n_landmarks=300, seed=seed)[:10],
    }


def _score(fa, fb):
    h1a = np.pad(fa["h1"], (0, max(0, 10 - len(fa["h1"]))))[:10]
    h1b = np.pad(fb["h1"], (0, max(0, 10 - len(fb["h1"]))))[:10]
    return (abs(fa["id"] - fb["id"])
            + 10.0 * _wass1(fa["hist"], fb["hist"])
            + 2.0 * float(np.abs(h1a - h1b).sum()))


def rank_candidates(data, n_boot=3, seed=0, candidates=None):
    """Return {name: mean score} — LOWER is better. Sorted dict."""
    candidates = candidates or CANDIDATES
    fd = fingerprint(np.asarray(data, float), seed=seed)
    out = {}
    for name, gen in candidates.items():
        s = [_score(fd, fingerprint(gen(n=2000, noise=0.02, seed=seed + 7 * b), seed=seed))
             for b in range(n_boot)]
        out[name] = float(np.mean(s))
    return dict(sorted(out.items(), key=lambda kv: kv[1]))
