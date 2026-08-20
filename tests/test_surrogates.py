"""Tests for the phase-randomized null (audit v2, F12)."""
import numpy as np

from tpl.nulls.surrogates import phase_randomize


def _signal(n=512, c=6, seed=0):
    """Broadband but strongly cross-correlated channels — the structure the null
    must be able to keep. Deliberately NOT a sum of a few sinusoids: at a single
    frequency, two random phases still give |corr| = |cos(dphi)|, which averages
    2/pi, so a narrowband signal cannot show decorrelation either way."""
    rng = np.random.default_rng(seed)
    kernel = np.exp(-np.linspace(-3, 3, 31) ** 2)
    kernel /= kernel.sum()
    base = np.convolve(rng.standard_normal(n + 60), kernel, mode="same")[30:30 + n]
    return np.stack([base + 0.05 * rng.standard_normal(n) for _ in range(c)], axis=1)


def _spectrum(x):
    return np.abs(np.fft.rfft(x, axis=0))


def _mean_abs_cross_corr(x):
    c = np.corrcoef(x.T)
    return float(np.abs(c[np.triu_indices_from(c, k=1)]).mean())


def test_power_spectrum_is_preserved():
    x = _signal()
    s = phase_randomize(x, seed=1)
    assert np.allclose(_spectrum(x), _spectrum(s), atol=1e-8)


def test_even_length_nyquist_bin_does_not_leak_power():
    """A random phase on the Nyquist bin is silently truncated by irfft, so the
    surrogate's spectrum stops matching the original."""
    for n in (512, 513):
        x = _signal(n=n)
        assert np.allclose(_spectrum(x), _spectrum(phase_randomize(x, seed=2)), atol=1e-8)


def test_default_keeps_cross_channel_correlation():
    x = _signal()
    s = phase_randomize(x, seed=3)
    assert abs(_mean_abs_cross_corr(s) - _mean_abs_cross_corr(x)) < 0.05


def test_independent_phases_destroy_cross_channel_correlation():
    """Why it is not the default: this null has already thrown away the coupling
    it is supposed to be a control for, so it loses for free."""
    x = _signal()
    s = phase_randomize(x, seed=3, preserve_cross=False)
    assert _mean_abs_cross_corr(x) > 0.9
    assert _mean_abs_cross_corr(s) < 0.3


def test_phases_are_actually_scrambled():
    x = _signal()
    assert not np.allclose(x, phase_randomize(x, seed=4), atol=1e-6)
