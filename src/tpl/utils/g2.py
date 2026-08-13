"""Derivations of the octonions = the Lie algebra g2, built numerically.

For x, y in O, D_{x,y} := [L_x, L_y] + [L_x, R_y] + [R_x, R_y] is a derivation
(Schafer, 'An Introduction to Nonassociative Algebras'). The span of all
D_{ei,ej} is g2 (dim 14). Derivations kill the real part and are antisymmetric
on Im(O) = R^7, so g2 sits inside so(7). The stabilizer subalgebra
{D in g2 : D(e7) = 0} is su(3) (dim 8). Both dimensions are *checked by tests*,
not assumed — this replaces hand-waving with computation (upgrade #5).
"""
import numpy as np
from tpl.utils.octonions import _TABLE


def _L(i):
    return _TABLE[i, :, :].T  # (L_x)[k,j] = T[i,j,k]


def _R(i):
    return _TABLE[:, i, :].T  # (R_x)[k,j] = T[j,i,k]


def _comm(a, b):
    return a @ b - b @ a


def derivation(i, j):
    """D_{ei,ej} restricted to Im(O) = R^7 (indices 1..7)."""
    Li, Lj, Ri, Rj = _L(i), _L(j), _R(i), _R(j)
    D = _comm(Li, Lj) + _comm(Li, Rj) + _comm(Ri, Rj)
    return D[1:, 1:]


def g2_basis(tol=1e-9):
    """Orthonormal basis of g2 as 7x7 matrices (expected dim: 14)."""
    vecs = [derivation(i, j).ravel() for i in range(1, 8) for j in range(i + 1, 8)]
    M = np.array(vecs).T  # 49 x 21
    U, s, _ = np.linalg.svd(M, full_matrices=False)
    r = int((s > tol * s[0]).sum())
    return [U[:, k].reshape(7, 7) for k in range(r)]


def su3_basis(fixed_index=6, tol=1e-9):
    """Basis of the stabilizer of e_{fixed_index+1} in g2 (expected dim: 8)."""
    B = g2_basis()
    A = np.array([D[:, fixed_index] for D in B]).T  # 7 x len(B): D(e_fixed)
    _, s, Vt = np.linalg.svd(A)
    ns = Vt[(s > tol * max(s[0], 1e-30)).sum():]  # null space coefficients
    return [sum(c * D for c, D in zip(row, B)) for row in ns]


def random_su3_generator(seed=0):
    rng = np.random.default_rng(seed)
    B = su3_basis()
    c = rng.standard_normal(len(B))
    D = sum(ci * Di for ci, Di in zip(c, B))
    return D / np.linalg.norm(D)
