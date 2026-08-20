"""The real-data extractor, without allensdk: duration budget and bridge rules."""
import numpy as np
import pytest

from tpl.io.extract import (MIN_RAW_DURATION_S, Block, extract_block,
                            is_powered, longest_named_block, report_power,
                            required_duration_s, select_units)


def _session(n_units=12, area="VISp", t_stop=120.0, rate=20.0, seed=0):
    rng = np.random.default_rng(seed)
    units = [{"id": i, "structure": area, "quality": "good"} for i in range(n_units)]
    spikes = {i: np.sort(rng.uniform(0, t_stop, size=int(rate * t_stop)))
              for i in range(n_units)}
    return spikes, units


def test_ten_second_percept_is_not_powered_even_at_lag_one():
    """The original H1 wording ('stimulus > 10 s') cannot hit n_min = 2000."""
    assert required_duration_s(n_min=2000, lag=1) == MIN_RAW_DURATION_S == 100.0
    assert not is_powered(10.0, lag=1)
    assert is_powered(100.0, lag=1)
    assert not is_powered(100.0, lag=5)


def test_grating_trials_do_not_become_powered_by_summing():
    """100 repeats of a 2 s grating look like 200 s if concatenated — forbidden."""
    presentations = [{"name": "drifting_gratings", "t_start": 2.0 * k,
                      "t_stop": 2.0 * k + 2.0} for k in range(100)]
    presentations.append({"name": "spontaneous", "t_start": 0.0, "t_stop": 1200.0})
    rows = {r["name"]: r for r in report_power(presentations)}
    assert rows["drifting_gratings"]["n_blocks"] == 100
    assert rows["drifting_gratings"]["sum_duration_s"] == 200.0
    assert rows["drifting_gratings"]["max_duration_s"] == 2.0
    assert rows["drifting_gratings"]["powered_lag1"] is False
    assert rows["spontaneous"]["powered_lag1"] is True
    assert rows["spontaneous"]["powered_lag10"] is True   # 1200 s >= 1000 s
    assert rows["spontaneous"]["powered_lag25"] is False  # needs 2500 s


def test_extract_refuses_a_short_block_rather_than_concatenating():
    spikes, units = _session(t_stop=30.0)
    with pytest.raises(ValueError, match="not powered"):
        extract_block(spikes, units, "VISp", Block("drifting_gratings", 0.0, 2.0))


def test_extract_bins_one_area_without_reducing_dimension():
    spikes, units = _session(n_units=12, t_stop=120.0)
    units.append({"id": 99, "structure": "LGd", "quality": "good"})
    spikes[99] = np.array([1.0, 2.0, 3.0])
    with pytest.warns(RuntimeWarning, match="INDECIDABLE"):
        X, labels = extract_block(spikes, units, "VISp", Block("spontaneous", 0.0, 120.0))
    assert X.shape[1] == 12
    assert X.shape[0] == 2400  # 120 s / 50 ms
    assert 99 not in set(labels)


def test_noise_units_are_dropped_good_units_are_not_rate_cut():
    units = [
        {"id": 0, "structure": "VISp", "quality": "good"},
        {"id": 1, "structure": "VISp", "quality": "noise"},
        {"id": 2, "structure": "VISp", "quality": "good"},
    ]
    assert select_units(units, "VISp") == [0, 2]


def test_longest_block_is_not_the_concatenation():
    presentations = [
        {"name": "spontaneous", "t_start": 0.0, "t_stop": 100.0},
        {"name": "spontaneous", "t_start": 500.0, "t_stop": 800.0},
    ]
    b = longest_named_block(presentations, "spontaneous")
    assert b.duration_s == 300.0
    assert b.t_start == 500.0


def test_too_few_units_in_the_area_is_refused():
    spikes, units = _session(n_units=5, t_stop=120.0)
    with pytest.warns(RuntimeWarning, match="INDECIDABLE"):
        with pytest.raises(ValueError, match="cannot sit"):
            extract_block(spikes, units, "VISp", Block("spontaneous", 0.0, 120.0))
