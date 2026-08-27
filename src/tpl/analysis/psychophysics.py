"""Chantier 8 analysis: MDS of a similarity matrix, then rival geometries.

This does NOT restore H1. Neural S6 on public Neuropixels is already
refuted; a perceptual sphere would be a different claim (docs/08).
CIELAB-like Euclidean colour is the strong null.
"""

import numpy as np

from tpl.analysis.manifold_evidence import _mds
from tpl.analysis.model_comparison import select_geometry


def dissimilarity_from_ratings(ratings):
    """ratings (n_stim, n_stim) higher = more similar → distance."""
    r = np.asarray(ratings, float)
    r = 0.5 * (r + r.T)
    d = r.max() - r
    np.fill_diagonal(d, 0.0)
    return np.maximum(d, 0.0)


def embed(dissimilarity, dim=3):
    return _mds(np.asarray(dissimilarity, float), dim)


def stress(dissimilarity, coords):
    d = np.asarray(dissimilarity, float)
    hat = np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=-1)
    iu = np.triu_indices_from(d, k=1)
    num = np.sum((d[iu] - hat[iu]) ** 2)
    den = np.sum(d[iu] ** 2)
    return float(np.sqrt(num / max(den, 1e-12)))


def rival_fit(dissimilarity, seed=0):
    """Stress of 3-D MDS vs unit-sphere projection vs the neural ranking.

    Colour psychophysics is 2–3 D, not S6. select_geometry on 12 points is
    underpowered and is stored only as a secondary label.
    """
    coords = embed(dissimilarity, dim=3)
    nrm = np.linalg.norm(coords, axis=1, keepdims=True)
    sphere = coords / np.maximum(nrm, 1e-12)
    out = {
        "stress_euclidean": stress(dissimilarity, coords),
        "stress_sphere": stress(dissimilarity, sphere),
        "n_stim": int(len(coords)),
    }
    if len(coords) >= 20:
        sel = select_geometry(coords, seed=seed, n_boot=2)
        out["geometry"] = sel["geometry"]
        out["fit_score"] = sel["score"]
    return out
