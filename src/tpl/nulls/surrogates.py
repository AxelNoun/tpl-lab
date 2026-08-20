"""Null #2: phase-randomized surrogates (same power spectrum, scrambled phases)."""
import numpy as np


def phase_randomize(x, seed=0, preserve_cross=True):
    """Surrogate with the same per-channel power spectrum and scrambled phases.

    `preserve_cross=True` draws ONE phase per frequency and applies it to every
    channel, which keeps the cross-spectrum — hence every linear inter-channel
    correlation and lag — intact. This is the null the project actually needs:
    it asks whether the observed geometry is more than linear coupling.

    `preserve_cross=False` draws an independent phase per channel, which also
    destroys inter-channel correlation. That is a null for 'any coupling at all',
    a far weaker opponent that a low-dimensional manifold beats for free. It was
    the original, undocumented default (audit v2, F12); kept only for the rare
    case where that is genuinely the intended comparison.

    The Nyquist bin of an even-length series must stay real, otherwise `irfft`
    silently discards an imaginary part and the surrogate's power spectrum no
    longer matches the original.
    """
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float)
    X = np.fft.rfft(x, axis=0)
    shape = (X.shape[0], 1) if preserve_cross else X.shape
    phases = np.broadcast_to(rng.uniform(0, 2 * np.pi, size=shape), X.shape).copy()
    phases[0] = 0.0
    if x.shape[0] % 2 == 0:
        phases[-1] = 0.0
    return np.fft.irfft(np.abs(X) * np.exp(1j * phases), n=x.shape[0], axis=0)
