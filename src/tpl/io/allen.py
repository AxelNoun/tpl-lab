"""Allen Brain Observatory — Visual Coding Neuropixels adapter (optional).

    python -m tpl.io.allen --nwb data/allen/session_767871931/session_767871931.nwb --list
    python -m tpl.io.allen --nwb data/allen/session_767871931/session_767871931.nwb \\
        --session 767871931 --area VISp --stimulus spontaneous \\
        --out data/real_VISp.npy

allensdk is an optional extra (`pip install -e ".[full]"`). This module is the
only one that imports it. Extraction rules live in `tpl.io.extract` and do not
depend on the SDK.

Allen Visual Coding is AWAKE only: there is no anesthesia condition here.
Trial-type stimuli (drifting gratings ~2 s) are shorter than the power floor;
the loader will refuse them rather than concatenate repeats.
"""
import argparse
import sys
from pathlib import Path

import numpy as np

from tpl.io.extract import (extract_block, longest_named_block, report_power,
                            MIN_RAW_DURATION_S, WARN_DURATION_S)


def _require_sdk():
    try:
        from allensdk.brain_observatory.ecephys.ecephys_project_cache import (
            EcephysProjectCache,
        )
    except ImportError as e:
        raise ImportError(
            "allensdk is an optional extra: pip install -e '.[full]'"
        ) from e
    return EcephysProjectCache


def open_cache(manifest):
    EcephysProjectCache = _require_sdk()
    return EcephysProjectCache.from_warehouse(manifest=str(manifest))


def units_from_session(session):
    """Translate the SDK table into the duck-typed list extract.py consumes.

    Frozen isolation filter: the SDK's own `quality` label, nothing else
    (no snr / isi_violations / firing_rate cut — those would be extra knobs).
    """
    table = session.units
    structure = (table["ecephys_structure_acronym"]
                 if "ecephys_structure_acronym" in table.columns
                 else table["structure_acronym"])
    quality = table["quality"] if "quality" in table.columns else None
    out = []
    for uid in table.index:
        rec = {"id": uid, "structure": structure.loc[uid]}
        if quality is not None:
            rec["quality"] = quality.loc[uid]
        out.append(rec)
    return out


def presentations_from_session(session):
    stim = session.stimulus_presentations
    name_col = "stimulus_name" if "stimulus_name" in stim.columns else "stimulus_block"
    return [{"name": row[name_col],
             "t_start": float(row["start_time"]),
             "t_stop": float(row["stop_time"])}
            for _, row in stim.iterrows()]


def _as_str(x):
    if isinstance(x, (bytes, np.bytes_)):
        return x.decode()
    return str(x)


def _ragged(data, index):
    """NWB VectorIndex: index[i] is the exclusive end of row i in `data`."""
    data, index = np.asarray(data), np.asarray(index, dtype=int)
    starts = np.concatenate(([0], index[:-1]))
    return [data[s:e] for s, e in zip(starts, index)]


def read_ecephys_nwb(path, spikes=True):
    """SDK-free reader for an Allen Visual Coding session NWB.

    pynwb/hdmf versions that ship with allensdk 2.16.2 refuse these 2019 files
    (`NWBFile.external_resources`). The extraction rules still live in
    extract.py; this only translates HDF5 tables into that duck type.
    Needs h5py (pulled in by allensdk, not a core dep).
    """
    try:
        import h5py
    except ImportError as e:
        raise ImportError("reading --nwb needs h5py: pip install h5py") from e

    path = Path(path)
    with h5py.File(path, "r") as f:
        session_id = _as_str(f["general/session_id"][()])
        try:
            session_id = int(session_id)
        except ValueError:
            pass

        el = f["general/extracellular_ephys/electrodes"]
        chan_to_loc = {int(i): _as_str(loc)
                       for i, loc in zip(el["id"][:], el["location"][:])}
        uids = np.asarray(f["units/id"][:])
        peak = np.asarray(f["units/peak_channel_id"][:])
        quality = [_as_str(q) for q in f["units/quality"][:]]
        units = [{"id": int(uid),
                  "structure": chan_to_loc.get(int(ch), ""),
                  "quality": q}
                 for uid, ch, q in zip(uids, peak, quality)]

        times_rows = _ragged(f["units/spike_times"][:],
                             f["units/spike_times_index"][:]) if spikes else []
        spike_times = ({int(uid): np.asarray(t, dtype=float)
                        for uid, t in zip(uids, times_rows)} if spikes else {})

        presentations = []
        for name in f["intervals"]:
            g = f["intervals"][name]
            if "start_time" not in g or "stop_time" not in g:
                continue
            starts, stops = g["start_time"][:], g["stop_time"][:]
            if "stimulus_name" in g:
                names = [_as_str(x) for x in g["stimulus_name"][:]]
            else:
                stem = name.removesuffix("_presentations")
                names = [stem] * len(starts)
            for nm, t0, t1 in zip(names, starts, stops):
                presentations.append({"name": nm, "t_start": float(t0),
                                      "t_stop": float(t1)})

    return {"session_id": session_id, "spike_times": spike_times,
            "units": units, "presentations": presentations}


def extract_from_nwb(path, area, stimulus="spontaneous"):
    rec = read_ecephys_nwb(path)
    block = longest_named_block(rec["presentations"], stimulus)
    X, labels = extract_block(rec["spike_times"], rec["units"], area, block)
    meta = {"session_id": rec["session_id"], "area": area, "stimulus": stimulus,
            "t_start": block.t_start, "t_stop": block.t_stop,
            "duration_s": block.duration_s, "n_windows": int(X.shape[0]),
            "n_units": int(X.shape[1]), "unit_ids": np.asarray(labels)}
    return X, meta


def extract_from_session(session, area, stimulus="spontaneous", session_id=None):
    presentations = presentations_from_session(session)
    block = longest_named_block(presentations, stimulus)
    units = units_from_session(session)
    X, labels = extract_block(session.spike_times, units, area, block)
    if session_id is None:
        session_id = getattr(session, "ecephys_session_id", None)
    meta = {"session_id": session_id, "area": area, "stimulus": stimulus,
            "t_start": block.t_start, "t_stop": block.t_stop,
            "duration_s": block.duration_s, "n_windows": int(X.shape[0]),
            "n_units": int(X.shape[1]), "unit_ids": np.asarray(labels)}
    return X, meta


def extract_session(cache, session_id, area, stimulus="spontaneous"):
    session = cache.get_session_data(int(session_id))
    return extract_from_session(session, area, stimulus, session_id=int(session_id))


def main(argv=None):
    p = argparse.ArgumentParser(description="Allen Neuropixels -> run_id array")
    p.add_argument("--manifest", help="warehouse manifest; unused if --nwb is set")
    p.add_argument("--nwb", help="local session NWB; skips LFP/movie warehouse files")
    p.add_argument("--session", type=int)
    p.add_argument("--area", help="exactly one structure acronym, e.g. VISp")
    p.add_argument("--stimulus", default="spontaneous",
                   help="stimulus name; the LONGEST single block is taken, "
                        "never concatenated")
    p.add_argument("--out", help="output .npy (not committed)")
    p.add_argument("--list", action="store_true",
                   help="print stimulus-block durations; no extract")
    p.add_argument("--seed", type=int, default=42, help="accepted, unused: no RNG here")
    a = p.parse_args(argv)

    print(f"[seed={a.seed}]  floor {MIN_RAW_DURATION_S:.0f} s (lag 1) ; "
          f"warning below {WARN_DURATION_S / 60:.0f} min")

    if a.nwb:
        rec = read_ecephys_nwb(a.nwb, spikes=not a.list)
        presentations, session, sid = rec["presentations"], None, rec["session_id"]
    else:
        if not a.manifest:
            p.error("--manifest is required unless --nwb is given")
        if a.session is None:
            p.error("--session is required when using --manifest")
        session = open_cache(a.manifest).get_session_data(int(a.session))
        presentations, sid = presentations_from_session(session), int(a.session)

    if a.list:
        rows = report_power(presentations)
        print(f"{'stimulus':<28s} {'max_s':>8s} {'n_blk':>6s} {'n_win':>8s}  "
              f"powered at lag 1 / 5 / 10 / 25 / 40")
        for r in rows:
            flags = " ".join("Y" if r[f"powered_lag{lag}"] else "."
                             for lag in (1, 5, 10, 25, 40))
            print(f"{r['name']:<28s} {r['max_duration_s']:8.1f} {r['n_blocks']:6d} "
                  f"{r['n_windows']:8d}  {flags}")
        print("duration = LONGEST single block, not the sum of trials. "
              "Y = enough windows to hit n_min=2000 at that lag, BEFORE "
              "measuring the actual autocorrelation. Concatenation is off.")
        return

    if a.area is None or a.out is None:
        p.error("--area and --out are required to extract")
    if a.nwb:
        block = longest_named_block(rec["presentations"], a.stimulus)
        X, labels = extract_block(rec["spike_times"], rec["units"], a.area, block)
        meta = {"session_id": rec["session_id"], "area": a.area,
                "stimulus": a.stimulus, "t_start": block.t_start,
                "t_stop": block.t_stop, "duration_s": block.duration_s,
                "n_windows": int(X.shape[0]), "n_units": int(X.shape[1]),
                "unit_ids": np.asarray(labels)}
    else:
        X, meta = extract_from_session(session, a.area, a.stimulus, session_id=sid)
    out = Path(a.out)
    if out.name.startswith("synth_"):
        p.error("this is a real recording; do not prefix synth_")
    out.parent.mkdir(parents=True, exist_ok=True)
    np.save(out, X)
    print(f"wrote {out}  shape {X.shape}  session {meta['session_id']}  "
          f"{meta['area']}  {meta['stimulus']}  {meta['duration_s']:.0f} s")
    print("next: python -m tpl.analysis.run_id --config configs/prereg_v1.json "
          f"--data {out}")
    return X, meta


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
