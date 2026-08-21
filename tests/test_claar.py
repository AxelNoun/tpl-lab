"""Claar wake/isoflurane adapter: epoch parsing, no NWB required."""
import numpy as np
import pytest

from tpl.io.claar import (coarse_modal_area, extract_state,
                          presentations_from_epochs)


def test_awake_is_the_clock_before_induction_not_a_concat_of_trials():
    rows = presentations_from_epochs(
        [100.0, 200.0], [200.0, 900.0],
        ["isoflurane_induction", "isoflurane_anesthesia"],
        t0=0.0,
    )
    by = {r["name"]: r for r in rows}
    assert by["awake"]["t_start"] == 0.0
    assert by["awake"]["t_stop"] == 100.0
    assert by["isoflurane_anesthesia"]["t_stop"] - by["isoflurane_anesthesia"]["t_start"] == 700.0
    assert by["isoflurane_induction"]["t_stop"] - by["isoflurane_induction"]["t_start"] == 100.0


def test_induction_is_not_used_as_anesthesia():
    rows = presentations_from_epochs(
        [0.0, 50.0], [50.0, 800.0],
        ["isoflurane_induction", "isoflurane_anesthesia"],
    )
    units = [{"id": i, "structure": "MOs", "quality": "good"} for i in range(8)]
    rng = np.random.default_rng(0)
    spikes = {i: np.sort(rng.uniform(0, 800, size=400)) for i in range(8)}
    with pytest.warns(RuntimeWarning, match="INDECIDABLE"):
        X, _ = extract_state(spikes, units, "MOs", rows, "isoflurane")
    # 750 s of maintained isoflurane, not 50 s of induction
    assert X.shape[0] == 15000


def test_short_awake_is_refused():
    rows = presentations_from_epochs(
        [10.0, 20.0], [20.0, 200.0],
        ["isoflurane_induction", "isoflurane_anesthesia"],
    )
    units = [{"id": i, "structure": "MOs", "quality": "good"} for i in range(8)]
    spikes = {i: np.array([0.1, 0.2]) for i in range(8)}
    with pytest.raises(ValueError, match="not powered"):
        extract_state(spikes, units, "MOs", rows, "awake")


def test_modal_area_folds_layers_and_ignores_noise():
    units = (
        [{"id": i, "structure": "MOs5", "quality": "good"} for i in range(5)]
        + [{"id": 10, "structure": "VISp6a", "quality": "good"}]
        + [{"id": 11, "structure": "MOs5", "quality": "noise"}]
    )
    assert coarse_modal_area(units) == "MOs"
