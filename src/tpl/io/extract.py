"""SDK-agnostic extraction: spikes + unit metadata -> population vectors.

No Allen, no pandas. The optional `tpl.io.allen` adapter is the only place
that talks to allensdk. Keeping this module numpy-only means the duration
budget and the 'one area, no concatenation' rules are tested without a 2 GB
dependency, and cannot drift when the SDK changes.
"""
from dataclasses import dataclass

import numpy as np

from tpl.analysis.bridge import WINDOW_MS, bin_population, prepare_population

# Absolute floor: 2000 windows of 50 ms if the series is already independent
# (lag = 1). Shorter than this cannot satisfy the prereg even in the best case.
MIN_RAW_DURATION_S = 2000 * (WINDOW_MS / 1000.0)  # 100 s

# The synthetic-flow lags of 25-55 do NOT transfer to 50 ms spike counts, so
# this is a warning, not a gate. run_id returns INDECIDABLE if n after
# decimation is still < 2000; that is the real floor.
WARN_DURATION_S = 45 * 60.0


def required_duration_s(n_min=2000, lag=1, window_ms=WINDOW_MS):
    """Recording length needed to have `n_min` independent windows at this lag."""
    return n_min * lag * (window_ms / 1000.0)


def is_powered(duration_s, n_min=2000, lag=1, window_ms=WINDOW_MS):
    return duration_s >= required_duration_s(n_min, lag, window_ms)


@dataclass(frozen=True)
class Block:
    name: str
    t_start: float
    t_stop: float

    @property
    def duration_s(self):
        return self.t_stop - self.t_start


def flatten_spikes(spike_times):
    """{unit_id: times_s} -> (times, unit_ids) for bin_population."""
    times, ids = [], []
    for uid, t in spike_times.items():
        t = np.asarray(t, dtype=float)
        times.append(t)
        ids.append(np.full(len(t), uid))
    if not times:
        return np.zeros(0), np.zeros(0, dtype=object)
    return np.concatenate(times), np.concatenate(ids)


def select_units(units, area, quality="good"):
    """Keep units in exactly one area. `quality` is an isolation label
    (Allen: 'good' vs 'noise'), not a firing-rate cut — rate thresholds are
    forbidden by the bridge law. Units missing a quality field are kept.
    """
    kept = []
    for u in units:
        if u["structure"] != area:
            continue
        q = u.get("quality")
        if q is not None and q != quality:
            continue
        kept.append(u["id"])
    if not kept:
        raise ValueError(f"no units in area {area!r} with quality={quality!r}")
    return kept


def extract_block(spike_times, units, area, block):
    """Population vectors for one area, one continuous time interval.

    Refuses concatenation: pass a single Block. Refuses short recordings that
    cannot hit n = 2000 even at lag = 1. Does not PCA, z-score, or rate-cut.
    """
    if block.duration_s < MIN_RAW_DURATION_S:
        raise ValueError(
            f"block {block.name!r} lasts {block.duration_s:.1f} s < "
            f"{MIN_RAW_DURATION_S:.0f} s (2000 windows of {WINDOW_MS} ms at lag 1). "
            f"A {block.duration_s:.1f} s 'constant percept' is not powered; do not "
            f"concatenate trials to invent duration (docs/13)."
        )
    if block.duration_s < WARN_DURATION_S:
        import warnings
        warnings.warn(
            f"block {block.name!r} lasts {block.duration_s / 60:.1f} min; after "
            f"decimation run_id may return INDECIDABLE (n_min = 2000). That is a "
            f"valid outcome, not a reason to loosen the floor.",
            RuntimeWarning,
            stacklevel=2,
        )
    keep = select_units(units, area)
    subset = {uid: np.asarray(spike_times.get(uid, []), dtype=float) for uid in keep}
    times, ids = flatten_spikes(subset)
    X, labels = bin_population(times, ids, block.t_start, block.t_stop)
    X = prepare_population(X)
    return X, labels


def longest_named_block(presentations, name):
    """Pick the longest continuous interval whose stimulus name matches.

    Presentations are NOT concatenated. Two 20 min spontaneous periods stay
    two blocks; the caller analyses them separately or picks one.
    """
    matches = [p for p in presentations if p["name"] == name]
    if not matches:
        available = sorted({p["name"] for p in presentations})
        raise ValueError(f"no block named {name!r}; available: {available}")
    blocks = [Block(p["name"], p["t_start"], p["t_stop"]) for p in matches]
    return max(blocks, key=lambda b: b.duration_s)


def report_power(presentations, n_min=2000, lags=(1, 5, 10, 25, 40)):
    """Power by stimulus name, using the LONGEST single block, not the sum.

    Summing 100 grating trials of 2 s would look powered and would be the
    concatenation the loader forbids.
    """
    by_name = {}
    for p in presentations:
        d = p["t_stop"] - p["t_start"]
        rec = by_name.setdefault(p["name"], {"name": p["name"], "n_blocks": 0,
                                             "max_duration_s": 0.0, "sum_duration_s": 0.0})
        rec["n_blocks"] += 1
        rec["max_duration_s"] = max(rec["max_duration_s"], d)
        rec["sum_duration_s"] += d
    rows = []
    for rec in by_name.values():
        d = rec["max_duration_s"]
        rows.append({
            **rec,
            "n_windows": int(d * 1000 / WINDOW_MS),
            **{f"powered_lag{lag}": is_powered(d, n_min=n_min, lag=lag) for lag in lags},
        })
    return sorted(rows, key=lambda r: -r["max_duration_s"])
