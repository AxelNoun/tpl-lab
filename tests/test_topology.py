from tpl.generative.manifolds import sphere, torus_flat
from tpl.analysis.topology import betti1

def test_sphere_has_no_loops():
    assert betti1(sphere(2000, dim=2, noise=0.02, seed=3), seed=3) == 0

def test_torus2_has_two_loops():
    assert betti1(torus_flat(2000, dim=2, noise=0.02, seed=3), seed=3) == 2

def test_conservative_in_high_dim():
    # Known low-power regime: must return 0 (no hallucinated loops), see calibration.
    assert betti1(torus_flat(2000, dim=6, noise=0.02, seed=3), seed=3) == 0
