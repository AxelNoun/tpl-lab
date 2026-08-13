import numpy as np
from tpl.analysis.intrinsic_dim import twonn
from tpl.generative.s6_flow import simulate_s6, sample_s6_uniform

def test_recovers_sphere_dim_iid():
    assert 5.2 < twonn(sample_s6_uniform(4000, seed=1)) < 6.8

def test_recovers_gaussian_dim():
    g = np.random.default_rng(1).standard_normal((4000, 8))
    assert 7.0 < twonn(g) < 9.0

def test_autocorrelation_biases_id_down():
    """Known pitfall: temporally correlated trajectories underestimate ID.
    Real-data pipelines MUST decorrelate (thinning / non-overlapping windows).
    Kept as a test so nobody 'fixes' it silently. See PREREGISTRATION.md."""
    traj = simulate_s6(n_steps=4000, seed=1)
    assert twonn(traj) < 5.0  # biased low, by design of the pitfall

def test_twonn_across_dimensions():
    from tpl.generative.manifolds import sphere
    for d in (2, 4):
        est = twonn(sphere(4000, dim=d, seed=6))
        assert abs(est - d) < 0.5
