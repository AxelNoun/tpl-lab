"""IBL adapter: same extract rules, no ONE-api required."""
import numpy as np
import pytest

from tpl.io.extract import longest_named_block
from tpl.io.ibl import (coarsen_to_area, extract_interval, extract_spontaneous,
                        ibl_area_matches, label_to_quality,
                        presentations_from_passive, spike_times_by_cluster,
                        units_from_clusters)


def test_visp_does_not_swallow_vispm():
    assert ibl_area_matches("VISp", "VISp")
    assert ibl_area_matches("VISp5", "VISp")
    assert ibl_area_matches("VISp6a", "VISp")
    assert ibl_area_matches("VISp2/3", "VISp")
    assert not ibl_area_matches("VISpm", "VISp")
    assert not ibl_area_matches("VISpl", "VISp")
    assert not ibl_area_matches("VISl", "VISp")


def test_ibl_label_one_is_good_not_a_rate_cut():
    assert label_to_quality(1) == "good"
    assert label_to_quality(0) == "noise"
    assert label_to_quality(3) == "noise"


def test_trials_are_not_in_the_passive_table():
    passive = {
        "spontaneousActivity": [100.0, 700.0],
        "RFM": [700.0, 900.0],
        "taskReplay": [900.0, 1100.0],
    }
    rows = presentations_from_passive(passive)
    b = longest_named_block(rows, "spontaneousActivity")
    assert b.duration_s == 600.0
    assert b.t_start == 100.0
    names = {r["name"] for r in rows}
    assert names == {"spontaneousActivity", "RFM", "taskReplay"}


def test_extract_spontaneous_one_area_layers_folded():
    rng = np.random.default_rng(0)
    t_stop = 120.0
    ids = [0, 1, 2, 3, 4, 5, 6, 7, 99]
    acr = ["VISp5", "VISp6a", "VISp", "VISpm", "VISp5", "VISp5", "VISp5", "VISp5", "CA1"]
    lab = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    units = coarsen_to_area(units_from_clusters(ids, acr, lab), "VISp")
    spikes = {i: np.sort(rng.uniform(0, t_stop, size=400)) for i in ids}
    presentations = presentations_from_passive(
        {"spontaneousActivity": [0.0, t_stop], "RFM": [t_stop, t_stop + 10]}
    )
    with pytest.warns(RuntimeWarning, match="INDECIDABLE"):
        X, labels = extract_spontaneous(spikes, units, "VISp", presentations)
    assert X.shape[1] == 7  # VISpm and CA1 out; seven VISp* good units
    assert 3 not in set(labels) and 99 not in set(labels)


def test_session_interval_is_one_clock_not_a_trial_union():
    rng = np.random.default_rng(1)
    units = units_from_clusters(range(8), ["VISp"] * 8, [1] * 8)
    spikes = {i: np.sort(rng.uniform(0, 400.0, size=800)) for i in range(8)}
    with pytest.warns(RuntimeWarning, match="INDECIDABLE"):
        X, _ = extract_interval(spikes, units, "VISp", 0.0, 400.0)
    assert X.shape == (8000, 8)


def test_short_spontaneous_is_refused_not_glued_to_rfm():
    units = units_from_clusters(range(8), ["VISp"] * 8, [1] * 8)
    spikes = {i: np.array([0.1, 0.2]) for i in range(8)}
    presentations = presentations_from_passive({
        "spontaneousActivity": [0.0, 20.0],
        "RFM": [20.0, 200.0],
    })
    with pytest.raises(ValueError, match="not powered"):
        extract_spontaneous(spikes, units, "VISp", presentations)


def test_csv_reader_long_layout(tmp_path):
    from tpl.io.ibl import _presentations_from_csv
    f = tmp_path / "long.csv"
    f.write_text("index,start,stop\nspontaneousActivity,10.0,130.0\nRFM,130.0,200.0\n")
    rows = {r["name"]: r for r in _presentations_from_csv(f)}
    assert rows["spontaneousActivity"]["t_stop"] - rows["spontaneousActivity"]["t_start"] == 120.0


def test_csv_reader_wide_ibl_layout(tmp_path):
    from tpl.io.ibl import _presentations_from_csv
    f = tmp_path / "passivePeriods.intervalsTable.csv"
    f.write_text(
        "Unnamed: 0,passiveProtocol,spontaneousActivity,RFM,taskReplay\n"
        "0,0,100.0,700.0,900.0\n"
        "1,1,700.0,900.0,1100.0\n"
    )
    rows = {r["name"]: r for r in _presentations_from_csv(f)}
    assert rows["spontaneousActivity"]["t_stop"] - rows["spontaneousActivity"]["t_start"] == 600.0
    assert "RFM" in rows and "taskReplay" in rows
    assert "passiveProtocol" not in rows


def test_spike_times_grouped_by_cluster():
    times = np.array([0.1, 0.2, 0.3, 0.4])
    clus = np.array([0, 1, 0, 1])
    d = spike_times_by_cluster(times, clus)
    np.testing.assert_allclose(d[0], [0.1, 0.3])
    np.testing.assert_allclose(d[1], [0.2, 0.4])
