"""Null #2: phase-randomized surrogates (same power spectrum, scrambled phases)."""
import numpy as np


def phase_randomize(x, seed=0):
    rng = np.random.default_rng(seed)
    X = np.fft.rfft(x, axis=0)
    phases = rng.uniform(0, 2 * np.pi, size=X.shape)
    phases[0] = 0.0
    Xs = np.abs(X) * np.exp(1j * phases)
    return np.fft.irfft(Xs, n=x.shape[0], axis=0)
