import numpy as np
from tpl.utils.octonions import om, associator, norm

def _e(i):
    v = np.zeros(8); v[i] = 1.0; return v

def test_fano_example():
    assert np.allclose(om(_e(1), _e(2)), _e(4))

def test_non_associative():
    a = associator(_e(1), _e(2), _e(3))
    assert norm(a) > 0.5  # octonions are not associative

def test_normed_division():
    rng = np.random.default_rng(0)
    for _ in range(20):
        x, y = rng.standard_normal(8), rng.standard_normal(8)
        assert np.isclose(norm(om(x, y)), norm(x) * norm(y), rtol=1e-10)

def test_alternativity():
    rng = np.random.default_rng(1)
    for _ in range(20):
        x, y = rng.standard_normal(8), rng.standard_normal(8)
        assert np.allclose(om(om(x, x), y), om(x, om(x, y)), atol=1e-12)
