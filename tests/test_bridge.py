"""Chantier 2 — the bridge law is a refusal to reduce, not a clever embedding."""
import numpy as np
import pytest

from tpl.analysis.bridge import bin_population, prepare_population, refuse_reduction
from tpl.analysis.spectral import covariance_spectrum, matches_s6_profile
from tpl.generative.manifolds import sphere


def test_binning_counts_spikes_per_window():
    times = np.array([0.01, 0.02, 0.06, 0.12])
    units = np.array([0, 0, 1, 0])
    X, labels = bin_population(times, units, 0.0, 0.15, window_ms=50)
    assert X.shape == (3, 2)
    assert X[0, 0] == 2  # two spikes of unit 0 in [0, 50ms)
    assert X[1, 1] == 1  # unit 1 in [50, 100ms)
    assert X[2, 0] == 1
    assert list(labels) == [0, 1]


def test_window_length_is_frozen():
    with pytest.raises(ValueError, match="frozen"):
        bin_population(np.array([0.0]), np.array([0]), 0.0, 1.0, window_ms=25)


def test_prepare_drops_silent_units_and_keeps_the_rest():
    X = np.zeros((100, 9))
    X[:, :7] = 1.0
    with pytest.warns(RuntimeWarning, match="never spiked"):
        Y = prepare_population(X)
    assert Y.shape == (100, 7)


def test_prepare_refuses_fewer_than_seven_channels():
    with pytest.raises(ValueError, match="cannot sit"):
        prepare_population(np.ones((50, 6)))


def test_refuse_reduction_blocks_pca_to_seven():
    with pytest.raises(ValueError, match="PCA to 7 is forbidden"):
        refuse_reduction(np.ones((100, 40)))


def test_spectral_profile_refuses_wrong_ambient_dimension():
    """A 20-D cloud used to be silently truncated to 35 eigenvalues."""
    rng = np.random.default_rng(0)
    cloud = rng.standard_normal((200, 20))
    with pytest.raises(ValueError, match="ambient dim is 20"):
        covariance_spectrum(cloud)
    assert matches_s6_profile(np.arange(40, dtype=float)) is False


def test_spectral_profile_still_matches_a_true_s6():
    ev = covariance_spectrum(sphere(8000, dim=6, seed=2))
    assert matches_s6_profile(ev)
    assert len(ev) == 35
