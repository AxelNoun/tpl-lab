"""The 'triplet phase closure' from the source article, implemented two ways.

(a) naive: phases per channel (Hilbert), closure = (a-b)+(b-c)+(c-a).
    Algebraically ZERO for any system. A tautology, not a test.
(b) windowed: each pairwise phase is estimated independently from the
    cross-spectrum per window. No longer identically zero -- but any coupled
    oscillator system (our Kuramoto null) keeps it small. Non-discriminating.
"""
import numpy as np
from scipy.signal import hilbert


def _analytic(x):
    return hilbert(x - x.mean(axis=0), axis=0)


def closure_naive(sig3):
    a = np.angle(_analytic(sig3))
    s = (a[:, 0] - a[:, 1]) + (a[:, 1] - a[:, 2]) + (a[:, 2] - a[:, 0])
    return np.abs(np.angle(np.exp(1j * s))).max()  # == 0 up to float error


def closure_windowed(sig3, win=200):
    z = _analytic(sig3)
    T = (z.shape[0] // win) * win
    z = z[:T].reshape(-1, win, 3)
    def pair(i, j):
        return np.angle((z[:, :, i] * np.conj(z[:, :, j])).sum(axis=1))
    s = pair(0, 1) + pair(1, 2) + pair(2, 0)
    err = np.abs(np.angle(np.exp(1j * s)))
    return float(err.mean())
