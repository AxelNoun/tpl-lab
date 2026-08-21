"""Chantier 4 — null model #3: the random recurrent network.

The hardest adversary this project has. Kuramoto and phase surrogates are not
built to produce a low-dimensional manifold; a chaotic RNN just past its
transition to chaos is, and it contains no S^6, no SU(3) and no octonions. If
the primary measures cannot tell it apart, they are measuring
low-dimensionality, not geometry.

x <- x + (1/tau)(-x + W tanh(x)) + noise, the Sompolinsky-Crisanti-Sommers
setup. g < 1 decays to zero; g > 1 is chaotic, with an attractor dimension that
grows with g.

Two low-rank variants were tried as adversaries and discarded (audit v2):
- W = g U V^T / N with independent U and V produces no dynamics at all. The
  feedback along mode k needs the overlap u_k . v_k / N, which vanishes for
  independent random vectors, so the network never leaves the noise-driven
  linear regime and reads d ~ 50-65: a 200-dimensional noise ball, not a
  manifold.
- W = g U U^T / N (symmetric) converges to fixed points, so the observed spread
  is again the full-dimensional noise ball: d ~ 58-70.
`simulate_lowrank_rnn` is the remaining Mastrogiuseppe & Ostojic construction:
structured m/n overlap (aligned or oscillatory pairs).
"""
import numpy as np


def structured_left_vectors(right, overlap, mode, rng):
    """Left vectors n given right vectors m (columns), as in Mastrogiuseppe 2018.

    `aligned`: n_r = ρ m_r + √(1-ρ²) ξ_r, so (m_r·n_r)/N → ρ. Rank-1 of this
    kind is bistable (the UU^T limit is ρ = 1).
    `oscillatory`: each pair (m_i, m_j) gets both a gain and a circulation,
    n_i = (ρ/√2)(m_i + m_j), n_j = (ρ/√2)(-m_i + m_j). Pure circulation
    (n_i = ρ m_j, n_j = -ρ m_i) has Jacobian eigenvalues -1 ± i gρ and
    dies into the origin; the aligned piece is what can Hopf-bifurcate.
    """
    if not 0.0 <= overlap <= 1.0:
        raise ValueError(f"overlap must be in [0, 1], got {overlap}")
    n_units, rank = right.shape
    leftover = float(np.sqrt(max(0.0, 1.0 - overlap * overlap)))
    left = leftover * rng.standard_normal((n_units, rank))
    if mode == "aligned":
        left += overlap * right
    elif mode == "oscillatory":
        s = overlap / np.sqrt(2.0)
        for k in range(rank // 2):
            i, j = 2 * k, 2 * k + 1
            left[:, i] += s * right[:, i] + s * right[:, j]
            left[:, j] += -s * right[:, i] + s * right[:, j]
        if rank % 2:
            left[:, -1] += overlap * right[:, -1]
    else:
        raise ValueError(f"unknown overlap mode {mode!r}")
    return left


def lowrank_weights(n_units, rank, overlap, mode="oscillatory", g_struct=4.0,
                    g_random=0.0, seed=0):
    """W = (g_struct / N) m n^T + (g_random / √N) Gaussian.

    The 1/N scaling is the low-rank mean-field one, not the chaotic 1/√N.
    """
    rng = np.random.default_rng(seed)
    right = rng.standard_normal((n_units, rank))
    left = structured_left_vectors(right, overlap, mode, rng)
    W = (g_struct / n_units) * (right @ left.T)
    if g_random:
        W = W + g_random * rng.standard_normal((n_units, n_units)) / np.sqrt(n_units)
    return W, right, left


def simulate_lowrank_rnn(n_units=200, n_steps=20000, rank=6, overlap=0.8,
                         mode="oscillatory", g_struct=4.0, g_random=0.0,
                         tau=10.0, noise=0.005, seed=0, burn_in=3000):
    """Low-rank RNN with structured m/n overlap. Shape (n_steps, n_units).

    Independent U,V (overlap = 0) and symmetric UU^T are not this function;
    they were measured and discarded (docs/RESULTATS_NEGATIFS.md).
    """
    W, _, _ = lowrank_weights(n_units, rank, overlap, mode=mode,
                              g_struct=g_struct, g_random=g_random, seed=seed)
    rng = np.random.default_rng(seed + 1)
    x = 0.5 * rng.standard_normal(n_units)
    out = np.empty((n_steps, n_units))
    for t in range(-burn_in, n_steps):
        x = x + (1.0 / tau) * (-x + W @ np.tanh(x)) \
            + noise * np.sqrt(1.0 / tau) * rng.standard_normal(n_units)
        if t >= 0:
            out[t] = x
    return out


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
