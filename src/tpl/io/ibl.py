"""IBL Brain-wide Map adapter (optional ONE-api / ibllib).

    python -m tpl.io.ibl --passive-csv path.csv --list
    python -m tpl.io.ibl --times spikes.times.npy --clusters spikes.clusters.npy \\
        --metrics clusters.npy --area VISp --out data/real_ibl_VISp.npy

Extraction rules live in `tpl.io.extract`. This module only translates IBL
tables into that duck type. It will not concatenate decision trials or glue
spontaneousActivity to RF mapping / task replay.

A result here cannot restore Allen H1-spontaneous (docs/17).
"""
import argparse
import sys
from pathlib import Path

import numpy as np

from tpl.io.extract import (extract_block, longest_named_block, report_power,
                            MIN_RAW_DURATION_S, WARN_DURATION_S)


def ibl_area_matches(acronym, area):
    """VISp includes VISp5 / VISp6a; it does not include VISpm or VISpl."""
    acronym, area = str(acronym), str(area)
    if acronym == area:
        return True
    extra = acronym[len(area):] if acronym.startswith(area) else None
    return bool(extra) and extra[0].isdigit()


def label_to_quality(label):
    """IBL published good units are label == 1. Not a firing-rate cut."""
    try:
        return "good" if int(label) == 1 else "noise"
    except (TypeError, ValueError):
        return "noise"


def units_from_clusters(cluster_ids, acronyms, labels):
    return [{"id": int(cid), "structure": str(acr),
             "quality": label_to_quality(lab)}
            for cid, acr, lab in zip(cluster_ids, acronyms, labels)]


def coarsen_to_area(units, area):
    """Rewrite matching layer acronyms to the requested area for select_units."""
    out = []
    for u in units:
        rec = dict(u)
        if ibl_area_matches(rec["structure"], area):
            rec["structure"] = area
        out.append(rec)
    return out


def spike_times_by_cluster(times, cluster_ids):
    times = np.asarray(times, dtype=float)
    cluster_ids = np.asarray(cluster_ids)
    out = {}
    for cid in np.unique(cluster_ids):
        out[int(cid)] = times[cluster_ids == cid]
    return out


def presentations_from_passive(passive):
    """`passivePeriods` table or mapping name -> [t_start, t_stop]."""
    rows = []
    if hasattr(passive, "items"):
        items = list(passive.items())
    else:
        raise TypeError("passive periods must be a mapping of name -> interval")
    for name, interval in items:
        interval = np.asarray(interval, dtype=float).reshape(-1)
        if interval.size < 2 or not np.isfinite(interval[:2]).all():
            continue
        rows.append({"name": str(name), "t_start": float(interval[0]),
                     "t_stop": float(interval[1])})
    return rows


def extract_spontaneous(spike_times, units, area, presentations,
                        stimulus="spontaneousActivity"):
    block = longest_named_block(presentations, stimulus)
    return extract_block(spike_times, coarsen_to_area(units, area), area, block)


def main(argv=None):
    p = argparse.ArgumentParser(description="IBL spikes -> run_id array")
    p.add_argument("--times", help="spikes.times.npy")
    p.add_argument("--clusters", help="spikes.clusters.npy")
    p.add_argument("--cluster-ids", help="optional clusters.uuids / id npy")
    p.add_argument("--acronyms", help="per-cluster CCF acronyms npy")
    p.add_argument("--labels", help="per-cluster IBL label npy (1 = good)")
    p.add_argument("--passive-csv", help="passivePeriods.intervalsTable.csv")
    p.add_argument("--area", help="CCF acronym, e.g. VISp (layers included)")
    p.add_argument("--stimulus", default="spontaneousActivity")
    p.add_argument("--out")
    p.add_argument("--list", action="store_true")
    p.add_argument("--seed", type=int, default=42, help="accepted, unused")
    a = p.parse_args(argv)

    print(f"[seed={a.seed}]  floor {MIN_RAW_DURATION_S:.0f} s (lag 1) ; "
          f"warning below {WARN_DURATION_S / 60:.0f} min")
    print("IBL: spontaneousActivity only; trials/ITI/RFM/replay are not glued.")

    presentations = None
    if a.passive_csv:
        presentations = _presentations_from_csv(a.passive_csv)

    if a.list:
        if presentations is None:
            p.error("--list needs --passive-csv")
        rows = report_power(presentations)
        print(f"{'stimulus':<28s} {'max_s':>8s} {'n_blk':>6s} {'n_win':>8s}  "
              f"powered at lag 1 / 5 / 10 / 25 / 40")
        for r in rows:
            flags = " ".join("Y" if r[f"powered_lag{lag}"] else "."
                             for lag in (1, 5, 10, 25, 40))
            print(f"{r['name']:<28s} {r['max_duration_s']:8.1f} {r['n_blocks']:6d} "
                  f"{r['n_windows']:8d}  {flags}")
        print("duration = LONGEST single block. Concatenation is off.")
        return

    if not all([a.times, a.clusters, a.acronyms, a.labels, a.area, a.out,
                presentations is not None]):
        p.error("extract needs --times --clusters --acronyms --labels "
                "--passive-csv --area --out")
    times = np.load(a.times)
    clus = np.load(a.clusters)
    acronyms = np.load(a.acronyms, allow_pickle=True)
    labels = np.load(a.labels)
    ids = (np.load(a.cluster_ids) if a.cluster_ids
           else np.arange(len(acronyms)))
    spike_times = spike_times_by_cluster(times, clus)
    units = units_from_clusters(ids, acronyms, labels)
    X, unit_ids = extract_spontaneous(spike_times, units, a.area, presentations,
                                      stimulus=a.stimulus)
    out = Path(a.out)
    if out.name.startswith("synth_"):
        p.error("this is a real recording; do not prefix synth_")
    out.parent.mkdir(parents=True, exist_ok=True)
    np.save(out, X)
    print(f"wrote {out}  shape {X.shape}  {a.area}  {a.stimulus}")
    print("next: python -m tpl.analysis.run_id --config configs/prereg_v1.json "
          f"--data {out}")
    return X, unit_ids


def _presentations_from_csv(path):
    """Read IBL `passivePeriods.intervalsTable.csv` without pandas.

    Two layouts exist:
    - long: name, start, stop per row
    - wide (current public BWM): two rows (start, stop) and one column per period
    """
    text = Path(path).read_text(encoding="utf-8")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return []
    header = [c.strip() for c in lines[0].split(",")]
    body = [[c.strip() for c in ln.split(",")] for ln in lines[1:]]
    header_l = [h.lower() for h in header]
    if "start" in header_l and "stop" in header_l:
        rows = []
        for parts in body:
            if len(parts) < 3 or not _looks_float(parts[-1]):
                continue
            rows.append({"name": parts[0], "t_start": float(parts[-2]),
                         "t_stop": float(parts[-1])})
        return rows
    skip = {"", "unnamed: 0", "index", "passiveprotocol"}
    out = []
    for j, name in enumerate(header):
        if name.lower() in skip:
            continue
        vals = [float(row[j]) for row in body
                if j < len(row) and _looks_float(row[j])]
        if len(vals) >= 2:
            out.append({"name": name, "t_start": vals[0], "t_stop": vals[1]})
    return out


def _looks_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
