"""Candidate geometries for strong inference (upgrade #4): the question is
'what IS the geometry of sustained percepts?', S^6 being one candidate."""
import numpy as np


def sphere(n=2000, dim=6, noise=0.0, seed=0):
    rng = np.random.default_rng(seed)
    x = rng.standard_normal((n, dim + 1))
    x /= np.linalg.norm(x, axis=1, keepdims=True)
    return x + noise * rng.standard_normal(x.shape)


def torus_flat(n=2000, dim=6, noise=0.0, seed=0):
    """Flat T^dim embedded in R^(2*dim), radii 1/sqrt(dim) (unit diameter)."""
    rng = np.random.default_rng(seed)
    ang = rng.uniform(0, 2 * np.pi, size=(n, dim))
    r = 1.0 / np.sqrt(dim)
    x = np.concatenate([r * np.cos(ang), r * np.sin(ang)], axis=1)
    return x + noise * rng.standard_normal(x.shape)


def euclidean(n=2000, dim=6, noise=0.0, seed=0):
    rng = np.random.default_rng(seed)
    x = rng.standard_normal((n, dim)) / np.sqrt(dim)
    return x + noise * rng.standard_normal(x.shape)


CANDIDATES = {"S6": sphere, "T6": torus_flat, "R6": euclidean}
