"""DANDI 000458 (Claar et al. 2023) wake vs isoflurane adapter.

    python -m tpl.io.claar --nwb path.nwb --list
    python -m tpl.io.claar --nwb path.nwb --area MOs --out-a data/real_claar_wake.npy \\
        --out-b data/real_claar_iso.npy

EEG-only NWBs in this dandiset have no `units` group and are refused.
Extraction rules live in `tpl.io.extract`.
"""
import argparse
import sys
from collections import Counter
from pathlib import Path

import numpy as np

from tpl.io.allen import _as_str, _ragged
from tpl.io.extract import (Block, extract_block, report_power,
                            MIN_RAW_DURATION_S, WARN_DURATION_S)
from tpl.io.ibl import coarsen_to_area


WAKE_NAMES = frozenset({"awake", "wakefulness", "wake"})
ANESTH_NAMES = frozenset({"isoflurane_anesthesia", "isoflurane", "anesthesia"})
INDUCTION_NAMES = frozenset({"isoflurane_induction", "induction"})


def presentations_from_epochs(starts, stops, tags, t0=0.0):
    """One row per epoch. Awake is the clock before induction if not tagged."""
    rows = []
    induction_start = None
    anesth_starts = []
    for t_start, t_stop, tag in zip(starts, stops, tags):
        name = str(tag).strip()
        rows.append({"name": name, "t_start": float(t_start),
                     "t_stop": float(t_stop)})
        key = name.lower()
        if key in INDUCTION_NAMES:
            induction_start = (float(t_start) if induction_start is None
                               else min(induction_start, float(t_start)))
        if key in ANESTH_NAMES:
            anesth_starts.append(float(t_start))
    if not any(r["name"].lower() in WAKE_NAMES for r in rows):
        hi = induction_start
        if hi is None and anesth_starts:
            hi = min(anesth_starts)
        if hi is not None and hi > t0:
            rows.append({"name": "awake", "t_start": float(t0), "t_stop": float(hi)})
    return rows


def coarse_stem(acronym):
    acr = str(acronym)
    i = len(acr)
    while i > 0 and (acr[i - 1].isdigit() or acr[i - 1] in "/"):
        i -= 1
    return acr[:i] if i else acr


def coarse_modal_area(units, quality="good"):
    counts = Counter()
    for u in units:
        q = u.get("quality")
        if q is not None and q != quality:
            continue
        counts[coarse_stem(u["structure"])] += 1
    if not counts:
        raise ValueError("no units to pick a modal area from")
    return counts.most_common(1)[0][0]


def _longest_named(presentations, names):
    names = {n.lower() for n in names}
    matches = [p for p in presentations if p["name"].lower() in names]
    if not matches:
        raise ValueError(f"no epoch in {sorted(names)}; "
                         f"available: {sorted({p['name'] for p in presentations})}")
    blocks = [Block(p["name"], p["t_start"], p["t_stop"]) for p in matches]
    return max(blocks, key=lambda b: b.duration_s)


def extract_state(spike_times, units, area, presentations, state):
    names = WAKE_NAMES if state == "awake" else ANESTH_NAMES
    block = _longest_named(presentations, names)
    return extract_block(spike_times, coarsen_to_area(units, area), area, block)


def read_claar_nwb(path, spikes=True):
    try:
        import h5py
    except ImportError as e:
        raise ImportError("reading --nwb needs h5py: pip install h5py") from e

    path = Path(path)
    with h5py.File(path, "r") as f:
        if "units" not in f:
            raise ValueError(f"{path} has no units group (EEG-only); "
                             "the spike bridge law refuses this file")
        u = f["units"]
        uids = np.asarray(u["id"][:]) if "id" in u else np.arange(u["spike_times_index"].shape[0])
        if "location" in u:
            structures = [_as_str(x) for x in u["location"][:]]
        else:
            el = f["general/extracellular_ephys/electrodes"]
            loc_col = "location" if "location" in el else None
            chan_to_loc = {}
            if loc_col:
                ids = el["id"][:] if "id" in el else np.arange(len(el[loc_col]))
                chan_to_loc = {int(i): _as_str(loc)
                               for i, loc in zip(ids, el[loc_col][:])}
            peak_key = next((k for k in ("peak_channel_id", "peak_channel")
                             if k in u), None)
            peak = np.asarray(u[peak_key][:]) if peak_key else np.zeros(len(uids), dtype=int)
            if peak.ndim > 1:
                peak = peak[:, 0]
            structures = [chan_to_loc.get(int(ch), "") for ch in peak]
        quality = ([_as_str(q) for q in u["quality"][:]] if "quality" in u
                   else [None] * len(uids))
        units = []
        for uid, struct, q in zip(uids, structures, quality):
            rec = {"id": int(uid), "structure": struct}
            if q is not None:
                rec["quality"] = q
            units.append(rec)
        spike_times = {}
        if spikes:
            rows = _ragged(u["spike_times"][:], u["spike_times_index"][:])
            spike_times = {int(uid): np.asarray(t, dtype=float)
                           for uid, t in zip(uids, rows)}
        starts = stops = tags = None
        if "intervals" in f and "epochs" in f["intervals"]:
            g = f["intervals/epochs"]
            starts, stops = g["start_time"][:], g["stop_time"][:]
            if "tags" in g:
                raw = g["tags"][:]
                if "tags_index" in g:
                    parts = _ragged(raw, g["tags_index"][:])
                    tags = [_as_str(p[0]) if len(p) else "epoch" for p in parts]
                else:
                    tags = [_as_str(x) for x in raw]
            else:
                tags = ["epoch"] * len(starts)
        t0 = 0.0
        presentations = presentations_from_epochs(
            starts if starts is not None else [],
            stops if stops is not None else [],
            tags if tags is not None else [],
            t0=t0,
        )
    return {"spike_times": spike_times, "units": units,
            "presentations": presentations}


def main(argv=None):
    p = argparse.ArgumentParser(description="Claar NWB -> wake/isoflurane arrays")
    p.add_argument("--nwb", required=True)
    p.add_argument("--area", help="CCF acronym; default = coarse modal area")
    p.add_argument("--out-a", help="wake .npy")
    p.add_argument("--out-b", help="isoflurane .npy")
    p.add_argument("--list", action="store_true")
    p.add_argument("--seed", type=int, default=42)
    a = p.parse_args(argv)

    print(f"[seed={a.seed}]  floor {MIN_RAW_DURATION_S:.0f} s ; "
          f"warning below {WARN_DURATION_S / 60:.0f} min")
    rec = read_claar_nwb(a.nwb, spikes=not a.list)
    if a.list:
        rows = report_power(rec["presentations"])
        print(f"{'epoch':<28s} {'max_s':>8s} {'n_blk':>6s}")
        for r in rows:
            print(f"{r['name']:<28s} {r['max_duration_s']:8.1f} {r['n_blocks']:6d}")
        print("duration = LONGEST single block. Concatenation is off.")
        return

    area = a.area or coarse_modal_area(rec["units"])
    print("area", area)
    if not a.out_a or not a.out_b:
        p.error("extract needs --out-a and --out-b")
    Xa, _ = extract_state(rec["spike_times"], rec["units"], area,
                          rec["presentations"], "awake")
    Xb, _ = extract_state(rec["spike_times"], rec["units"], area,
                          rec["presentations"], "isoflurane")
    for path, X, label in ((a.out_a, Xa, "wake"), (a.out_b, Xb, "isoflurane")):
        out = Path(path)
        if out.name.startswith("synth_"):
            p.error("this is a real recording; do not prefix synth_")
        out.parent.mkdir(parents=True, exist_ok=True)
        np.save(out, X)
        print(f"wrote {out}  {label}  shape {X.shape}")
    print("next: python -m tpl.analysis.run_id --config configs/prereg_v1.json "
          f"--data {a.out_a} --data-b {a.out_b} --seed {a.seed}")


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
