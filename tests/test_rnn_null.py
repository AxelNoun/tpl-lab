"""The RNN null must lose, and must lose for the right reason (chantier 4)."""
import numpy as np
import pytest

from tpl.analysis.intrinsic_dim import autocorrelation_time, decorrelate, twonn
from tpl.analysis.model_comparison import select_geometry
from tpl.nulls.rnn import (lowrank_weights, rnn_readout, simulate_lowrank_rnn,
                           simulate_rnn, structured_left_vectors)


def test_subcritical_network_decays():
    """g < 1: no sustained dynamics, so nothing to measure."""
    traj = simulate_rnn(n_units=100, n_steps=3000, g=0.5, seed=0)
    assert np.abs(traj).mean() < 0.05


def test_chaotic_network_sustains_activity():
    traj = simulate_rnn(n_units=100, n_steps=3000, g=2.0, seed=0)
    assert np.abs(traj).mean() > 0.2


def test_readout_preserves_dimension():
    """The random projection must not itself create or destroy structure."""
    traj = simulate_rnn(n_units=100, n_steps=6000, g=1.6, seed=0)
    assert rnn_readout(traj, n_channels=7, seed=0).shape == (6000, 7)


def test_null_is_rejected_by_the_geometry_measure():
    """The point of the whole module: a network with no S6 in it must not be
    accepted as S6. Measured scores run 15-32 against a cutoff of 3.0."""
    traj = simulate_rnn(n_units=100, n_steps=25000, g=1.5, seed=0)
    thinned, _ = decorrelate(traj)
    sel = select_geometry(thinned, seed=0)
    assert sel["geometry"] is None
    assert sel["score"] > 3.0


def test_undecorrelatable_series_warns():
    """Regression, audit v2: hitting the lag cap used to pass silently, and a
    chaotic RNN at g = 1.8 then read d = 6.14 on 140 samples that were never
    independent — a confirmation manufactured out of autocorrelation."""
    t = np.linspace(0, 4 * np.pi, 800)
    smooth = np.stack([np.sin(t + k) for k in range(5)], axis=1)
    with pytest.warns(RuntimeWarning, match="never fell below"):
        autocorrelation_time(smooth, max_lag=20)


def test_aligned_overlap_is_the_mean_field_rho():
    rng = np.random.default_rng(0)
    m = rng.standard_normal((2000, 1))
    n = structured_left_vectors(m, overlap=0.7, mode="aligned", rng=rng)
    rho = float((m[:, 0] @ n[:, 0]) / m.shape[0])
    assert abs(rho - 0.7) < 0.05


def test_zero_overlap_has_no_collective_mode():
    """The independent-U,V dead end: projection on m is noise-sized."""
    W, m, n = lowrank_weights(200, rank=1, overlap=0.0, mode="aligned",
                              g_struct=4.0, seed=0)
    traj = simulate_lowrank_rnn(n_units=200, n_steps=4000, rank=1, overlap=0.0,
                                mode="aligned", g_struct=4.0, seed=0, burn_in=500)
    along_m = traj @ (m[:, 0] / np.linalg.norm(m[:, 0]))
    rng = np.random.default_rng(1)
    rand = rng.standard_normal(200)
    along_rand = traj @ (rand / np.linalg.norm(rand))
    assert along_m.std() < 3.0 * along_rand.std() + 0.05


def test_oscillatory_rank2_circulates_instead_of_sticking():
    """Gain plus circulation in the (m1, m2) plane: the latent must keep moving."""
    W, m, _ = lowrank_weights(200, rank=2, overlap=0.9, mode="oscillatory",
                              g_struct=4.0, seed=0)
    traj = simulate_lowrank_rnn(n_units=200, n_steps=8000, rank=2, overlap=0.9,
                                mode="oscillatory", g_struct=4.0, seed=0,
                                burn_in=2000)
    Q, _ = np.linalg.qr(m)
    lat = traj @ Q
    # a fixed point has tiny temporal std; a cycle does not
    assert lat.std(axis=0).min() > 0.05
    # late vs early: the orbit still has radius
    r_late = np.linalg.norm(lat[-2000:], axis=1).mean()
    assert r_late > 0.1


def test_lowrank_null_is_not_named_s6():
    """A rank-6 circulating RNN has no S6 in it. Cheap n, same cutoff."""
    traj = simulate_lowrank_rnn(n_units=120, n_steps=25000, rank=6, overlap=0.8,
                                mode="oscillatory", g_struct=4.0, seed=0)
    thinned, _ = decorrelate(traj)
    if len(thinned) < 200:
        pytest.skip("undecorrelatable at this length; run_id would be INDECIDABLE")
    sel = select_geometry(thinned, seed=0)
    assert sel["geometry"] != "S6"


def test_dimension_is_not_tunable_towards_six():
    """`g` does not let anyone dial this null onto the prediction: the estimate
    moves non-monotonically and lands nowhere near 6 at either end. Measured on
    a 200-unit network with enough independent samples: 12.4 / 9.6 / 3.4 at
    g = 1.4 / 1.5 / 1.6. Cheap version of the same check."""
    thin_low, _ = decorrelate(simulate_rnn(n_units=100, n_steps=25000, g=1.3, seed=0))
    thin_high, _ = decorrelate(simulate_rnn(n_units=100, n_steps=25000, g=2.0, seed=0))
    assert not (5.5 <= twonn(thin_low) < 6.5)
    assert not (5.5 <= twonn(thin_high) < 6.5)
