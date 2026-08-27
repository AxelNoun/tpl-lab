"""Chantier 8: MDS of synthetic similarity, CIELAB-like null."""
import numpy as np

from tpl.analysis.psychophysics import (
    dissimilarity_from_ratings,
    embed,
    rival_fit,
    stress,
)
from tpl.generative.manifolds import euclidean, sphere


def test_sphere_chordal_is_already_euclidean_in_r3():
    """S^2 chordal distances live in R^3: the CIELAB-like null is strong."""
    pts = sphere(24, dim=2, noise=0.0, seed=3)
    d = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=-1)
    fit = rival_fit(dissimilarity_from_ratings(d.max() - d), seed=3)
    assert fit["stress_euclidean"] < 0.05
    assert fit["n_stim"] == 24


def test_euclidean_judgments_do_not_need_a_sphere():
    pts = euclidean(24, dim=3, noise=0.02, seed=4)
    d = np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=-1)
    fit = rival_fit(d, seed=4)
    assert fit["stress_euclidean"] <= fit["stress_sphere"] + 0.02
    assert embed(d, dim=3).shape == (24, 3)
    assert stress(d, embed(d, dim=3)) < 0.3
