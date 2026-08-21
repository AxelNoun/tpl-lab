"""h5py reader for Allen session NWB (no pynwb). Skips if h5py is absent."""
import numpy as np
import pytest

h5py = pytest.importorskip("h5py")

from tpl.io.allen import read_ecephys_nwb
from tpl.io.extract import longest_named_block, select_units


def _mini_nwb(path):
    with h5py.File(path, "w") as f:
        f.create_dataset("general/session_id", data="1")
        el = f.create_group("general/extracellular_ephys/electrodes")
        el.create_dataset("id", data=np.array([10, 11], dtype=np.int64))
        el.create_dataset("location", data=np.array([b"VISp", b"CA1"]))
        u = f.create_group("units")
        u.create_dataset("id", data=np.array([1, 2, 3], dtype=np.int64))
        u.create_dataset("peak_channel_id", data=np.array([10, 10, 11], dtype=np.int64))
        u.create_dataset("quality", data=np.array([b"good", b"noise", b"good"]))
        times = np.array([0.1, 0.2, 5.0, 0.3], dtype=float)
        u.create_dataset("spike_times", data=times)
        u.create_dataset("spike_times_index", data=np.array([2, 3, 4], dtype=np.int64))
        sp = f.create_group("intervals/spontaneous_presentations")
        sp.create_dataset("start_time", data=np.array([0.0, 10.0]))
        sp.create_dataset("stop_time", data=np.array([2.0, 40.0]))
        sp.create_dataset("stimulus_name", data=np.array([b"spontaneous", b"spontaneous"]))
        gr = f.create_group("intervals/gabors_presentations")
        gr.create_dataset("start_time", data=np.array([2.0, 2.3]))
        gr.create_dataset("stop_time", data=np.array([2.3, 2.6]))
        gr.create_dataset("stimulus_name", data=np.array([b"gabors", b"gabors"]))


def test_read_ecephys_nwb_does_not_concatenate(tmp_path):
    path = tmp_path / "mini.nwb"
    _mini_nwb(path)
    rec = read_ecephys_nwb(path)
    block = longest_named_block(rec["presentations"], "spontaneous")
    assert block.duration_s == 30.0
    assert block.t_start == 10.0
    keep = select_units(rec["units"], "VISp")
    assert keep == [1]


def test_ragged_spike_times_split_by_unit(tmp_path):
    path = tmp_path / "mini.nwb"
    _mini_nwb(path)
    rec = read_ecephys_nwb(path)
    np.testing.assert_allclose(rec["spike_times"][1], [0.1, 0.2])
    np.testing.assert_allclose(rec["spike_times"][2], [5.0])
