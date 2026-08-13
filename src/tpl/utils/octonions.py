"""Octonion arithmetic via the Fano plane. Basis: e0=1, e1..e7 imaginary.

Purpose in this project: make non-associativity a *computable object* (the
associator), so nobody confuses it with phase statistics (see docs/03).
"""
import numpy as np

# Fano triples (a,b,c): ea*eb = ec (cyclic), anti-commutative, ei^2 = -1.
_FANO = [(1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 7), (5, 6, 1), (6, 7, 2), (7, 1, 3)]

_TABLE = np.zeros((8, 8, 8))  # _TABLE[i, j] = vector of e_i * e_j
_TABLE[0, :, :] = np.eye(8)
_TABLE[:, 0, :] = np.eye(8)
for i in range(1, 8):
    _TABLE[i, i, 0] = -1.0
for a, b, c in _FANO:
    for x, y, z in ((a, b, c), (b, c, a), (c, a, b)):
        _TABLE[x, y, z] = 1.0
        _TABLE[y, x, z] = -1.0


def om(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Octonion multiplication of 8-vectors."""
    return np.einsum("i,j,ijk->k", x, y, _TABLE)


def associator(x, y, z):
    """(xy)z - x(yz). Nonzero in general: octonions are NOT associative."""
    return om(om(x, y), z) - om(x, om(y, z))


def norm(x):
    return float(np.linalg.norm(x))
