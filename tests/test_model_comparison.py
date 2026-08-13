from tpl.generative.manifolds import sphere, torus_flat
from tpl.analysis.model_comparison import rank_candidates

def test_s6_data_ranked_s6():
    assert next(iter(rank_candidates(sphere(2000, dim=6, noise=0.03, seed=1), seed=1))) == "S6"

def test_t6_data_ranked_t6():
    assert next(iter(rank_candidates(torus_flat(2000, dim=6, noise=0.03, seed=1), seed=1))) == "T6"
