"""Chantier 4 — null model #1: the plain Kuramoto oscillator network.

If a proposed 'signature of consciousness geometry' also shows up here, the
signature is non-discriminating. That is the whole point of this module.
"""
import numpy as np


def simulate_kuramoto(n=12, K=2.0, n_steps=4000, dt=0.01, noise=0.05, seed=0):
    rng = np.random.default_rng(seed)
    omega = rng.normal(2 * np.pi * 1.0, 0.5, size=n)  # ~1 Hz spread
    theta = rng.uniform(0, 2 * np.pi, size=n)
    thetas = np.empty((n_steps, n))
    for t in range(n_steps):
        coupling = np.sin(theta[None, :] - theta[:, None]).sum(axis=1)
        theta = theta + dt * (omega + (K / n) * coupling) + np.sqrt(dt) * noise * rng.standard_normal(n)
        thetas[t] = theta
    return thetas


def order_parameter(thetas):
    return np.abs(np.exp(1j * thetas).mean(axis=1)).mean()
