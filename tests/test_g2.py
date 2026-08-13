import numpy as np
from tpl.utils.g2 import g2_basis, su3_basis, random_su3_generator

def test_g2_dimension_is_14():
    assert len(g2_basis()) == 14

def test_su3_dimension_is_8():
    assert len(su3_basis()) == 8

def test_su3_generator_properties():
    D = random_su3_generator(0)
    assert np.linalg.norm(D + D.T) < 1e-12          # in so(7)
    e7 = np.zeros(7); e7[6] = 1
    assert np.linalg.norm(D @ e7) < 1e-12           # stabilizes e7

def test_derivations_satisfy_leibniz():
    """THE defining property D(ab) = D(a)b + a D(b) — added after audit v1."""
    from tpl.utils.g2 import _L, _R, _comm
    from tpl.utils.octonions import om
    rng = np.random.default_rng(2)
    for i, j in [(1, 2), (3, 5), (2, 7)]:
        D = _comm(_L(i), _L(j)) + _comm(_L(i), _R(j)) + _comm(_R(i), _R(j))
        for _ in range(5):
            a, b = rng.standard_normal(8), rng.standard_normal(8)
            assert np.abs(D @ om(a, b) - om(D @ a, b) - om(a, D @ b)).max() < 1e-12

def test_su3_closed_under_bracket():
    S = su3_basis()
    V = np.array([X.ravel() for X in S]).T
    P = V @ np.linalg.pinv(V)
    for a in range(8):
        for b in range(a + 1, 8):
            br = (S[a] @ S[b] - S[b] @ S[a]).ravel()
            assert np.abs((np.eye(49) - P) @ br).max() < 1e-12
