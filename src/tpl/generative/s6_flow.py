"""Chantier 3 — generative model on S^6 (unit sphere in R^7).

Two dynamics, both renormalized to the sphere:

- ``simulate_s6``: generic SO(7) rotation plus tangential Brownian motion.
  Ground-truth intrinsic dimension 6 for the pipeline.
- ``simulate_su3_flow``: drift from a genuine su(3) generator (octonion-derived
  g2, see ``tpl.utils.g2``) plus transverse noise so the process covers S^6.
  Pure SU(3) holonomy is not a passive test (chantier 5).
"""
import numpy as np


def simulate_s6(n_steps=3000, dt=0.02, noise=0.6, seed=0):
    rng = np.random.default_rng(seed)
    A = rng.standard_normal((7, 7))
    A = (A - A.T) / 2.0  # antisymmetric -> rotation generator
    x = rng.standard_normal(7)
    x /= np.linalg.norm(x)
    out = np.empty((n_steps, 7))
    for t in range(n_steps):
        drift = A @ x
        w = rng.standard_normal(7) * noise
        w -= (w @ x) * x  # project noise onto tangent space
        x = x + dt * drift + np.sqrt(dt) * w
        x /= np.linalg.norm(x)
        out[t] = x
    return out


def observe(traj, n_channels=8, snr=5.0, seed=0):
    """Realistic-ish measurement: random linear mixing + sensor noise."""
    rng = np.random.default_rng(seed)
    M = rng.standard_normal((traj.shape[1], n_channels))
    y = traj @ M
    y += rng.standard_normal(y.shape) * (y.std() / snr)
    return y


def sample_s6_uniform(n=4000, seed=0):
    """I.i.d. uniform sample on S^6 (ground truth d=6 for pipeline validation)."""
    rng = np.random.default_rng(seed)
    x = rng.standard_normal((n, 7))
    return x / np.linalg.norm(x, axis=1, keepdims=True)


def simulate_su3_flow(n_steps=4000, dt=0.02, noise=0.6, seed=0):
    """Drift = a genuine su(3) generator (from the octonion-derived g2, see
    tpl.utils.g2) + tangential diffusion. Pure su(3) orbits foliate S^6 into
    S^5 leaves (SU(3)/SU(2)); the transverse noise explores the G2/SU(3)
    direction so the process covers S^6. Replaces the earlier placeholder."""
    from tpl.utils.g2 import random_su3_generator
    rng = np.random.default_rng(seed)
    D = random_su3_generator(seed) * 3.0
    x = rng.standard_normal(7)
    x /= np.linalg.norm(x)
    out = np.empty((n_steps, 7))
    for t in range(n_steps):
        w = rng.standard_normal(7) * noise
        w -= (w @ x) * x
        x = x + dt * (D @ x) + np.sqrt(dt) * w
        x /= np.linalg.norm(x)
        out[t] = x
    return out
