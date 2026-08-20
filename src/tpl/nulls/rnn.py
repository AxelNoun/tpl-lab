"""Chantier 4 — null model #3: the random recurrent network.

The hardest adversary this project has. Kuramoto and phase surrogates are not
built to produce a low-dimensional manifold; a chaotic RNN just past its
transition to chaos is, and it contains no S^6, no SU(3) and no octonions. If
the primary measures cannot tell it apart, they are measuring
low-dimensionality, not geometry.

x <- x + (1/tau)(-x + W tanh(x)) + noise, the Sompolinsky-Crisanti-Sommers
setup. g < 1 decays to zero; g > 1 is chaotic, with an attractor dimension that
grows with g.

Two low-rank variants were tried as adversaries and are NOT offered here,
because measurement showed neither is one (audit v2):
- W = g U V^T / N with independent U and V produces no dynamics at all. The
  feedback along mode k needs the overlap u_k . v_k / N, which vanishes for
  independent random vectors, so the network never leaves the noise-driven
  linear regime and reads d ~ 50-65: a 200-dimensional noise ball, not a
  manifold.
- W = g U U^T / N (symmetric) converges to fixed points, so the observed spread
  is again the full-dimensional noise ball: d ~ 58-70.
Getting genuine low-rank dynamics requires structured u/v overlap
(Mastrogiuseppe & Ostojic 2018) and is left for a later pass.
"""
import numpy as np


def simulate_rnn(n_units=200, n_steps=20000, g=1.5, tau=10.0, noise=0.005,
                 seed=0, burn_in=3000):
    """Trajectory of a chaotic random RNN, shape (n_steps, n_units).

    `g` is the only knob that matters and it does NOT tune towards d = 6: the
    measured intrinsic dimension jumps 12.4 -> 9.6 -> 3.4 across g = 1.4, 1.5,
    1.6, and at g = 1.8 the trajectory stops being decorrelatable altogether.
    """
    rng = np.random.default_rng(seed)
    W = g * rng.standard_normal((n_units, n_units)) / np.sqrt(n_units)
    x = 0.5 * rng.standard_normal(n_units)
    out = np.empty((n_steps, n_units))
    for t in range(-burn_in, n_steps):
        x = x + (1.0 / tau) * (-x + W @ np.tanh(x)) \
            + noise * np.sqrt(1.0 / tau) * rng.standard_normal(n_units)
        if t >= 0:
            out[t] = x
    return out


def rnn_readout(traj, n_channels=7, seed=0):
    """Random linear readout, the same 'realistic projection' the generative
    model gets from tpl.generative.s6_flow.observe. Keeps the comparison fair:
    both sides are seen through an arbitrary linear mixture rather than in
    privileged coordinates."""
    rng = np.random.default_rng(seed)
    M = rng.standard_normal((traj.shape[1], n_channels)) / np.sqrt(traj.shape[1])
    return traj @ M
