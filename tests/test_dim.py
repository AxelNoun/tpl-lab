import numpy as np
import pytest
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

def test_duplicates_do_not_inflate_dimension():
    """Regression, audit v2: duplicated points used to read d ~ 9 on true d = 6.
    Their neighbours get r2/r1 = 1 exactly, which adds nothing to the fit but
    still consumes rank in the empirical CDF."""
    pts = sample_s6_uniform(2000, seed=3)
    resampled = pts[np.random.default_rng(0).choice(len(pts), len(pts), replace=True)]
    with pytest.warns(RuntimeWarning, match="duplicate"):
        est = twonn(resampled)
    assert 5.0 < est < 7.0, "duplicates must not inflate the estimate"
    # dropping duplicates is exactly what the dedupe path does
    assert est == twonn(np.unique(resampled, axis=0), dedupe=False)

def test_dedupe_is_a_noop_without_duplicates():
    pts = sample_s6_uniform(1500, seed=8)
    assert twonn(pts, dedupe=True) == twonn(pts, dedupe=False)
