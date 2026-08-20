import numpy as np
from tpl.generative.manifolds import sphere, torus_flat
from tpl.analysis.model_comparison import (rank_candidates, fingerprint, _score,
                                           select_geometry, MAX_FIT_SCORE)

def test_s6_data_ranked_s6():
    assert next(iter(rank_candidates(sphere(2000, dim=6, noise=0.03, seed=1), seed=1))) == "S6"

def test_t6_data_ranked_t6():
    assert next(iter(rank_candidates(torus_flat(2000, dim=6, noise=0.03, seed=1), seed=1))) == "T6"

def test_fingerprint_is_scale_invariant():
    """Regression, audit v2: H1 persistences were taken on raw points, so the
    same cloud in different units scored 5.0 against itself instead of 0.
    Real recordings have no natural unit, so any absolute goodness-of-fit
    threshold depends on this holding."""
    p = sphere(1500, dim=6, noise=0.03, seed=1)
    assert _score(fingerprint(p, seed=1), fingerprint(p * 7.0, seed=1)) < 1e-6

def test_ranking_is_scale_invariant():
    p = sphere(1500, dim=6, noise=0.03, seed=1)
    plain = rank_candidates(p, seed=1)
    scaled = rank_candidates(p * 7.0, seed=1)
    assert next(iter(plain)) == next(iter(scaled)) == "S6"
    assert abs(plain["S6"] - scaled["S6"]) < 1e-6

def test_true_geometry_is_accepted():
    for gen, expected in [(sphere, "S6"), (torus_flat, "T6")]:
        sel = select_geometry(gen(2000, dim=6, noise=0.03, seed=1), seed=1)
        assert sel["accepted"] and sel["geometry"] == expected
        assert sel["score"] <= MAX_FIT_SCORE

def test_wrong_dimension_is_rejected():
    """Regression, audit v2 F3: rank_candidates alone called S^3 data 'R6'.
    The honest answer is that none of S6/T6/R6 fits."""
    sel = select_geometry(sphere(2000, dim=3, noise=0.03, seed=1), seed=1)
    assert sel["geometry"] is None and not sel["accepted"]

def test_noise_is_rejected():
    data = np.random.default_rng(1).standard_normal((2000, 20)) / np.sqrt(20)
    sel = select_geometry(data, seed=1)
    assert sel["geometry"] is None, "20-D noise used to be declared T6"
