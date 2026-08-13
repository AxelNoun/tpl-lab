import numpy as np
from tpl.generative.manifolds import sphere
from tpl.analysis.spectral import (covariance_spectrum, matches_s6_profile,
                                   THEORY_S6, schur_block_scores)

def test_exact_four_level_theory():
    ev = covariance_spectrum(sphere(20000, dim=6, seed=2))
    for sl, t in [(slice(0,7),1/7),(slice(7,13),2/63),(slice(13,34),1/63)]:
        assert abs(ev[sl].mean() - t) < 0.1 * t
    assert abs(ev[34]) < 1e-3

def test_profile_match_discriminates():
    assert matches_s6_profile(covariance_spectrum(sphere(20000, dim=6, seed=2)))
    g = np.random.default_rng(0).standard_normal((20000, 7)) / np.sqrt(7)
    assert not matches_s6_profile(covariance_spectrum(g))

def test_schur_invariance_vs_anisotropy():
    pts = sphere(20000, dim=6, seed=3)
    iso = schur_block_scores(pts)
    stretched = pts * np.array([2.0,1,1,1,1,1,1])  # anisotropic deformation
    ani = schur_block_scores(stretched / np.linalg.norm(stretched, axis=1, keepdims=True))
    assert iso["H2"] < 0.1 and ani["H2"] > 3 * iso["H2"]
