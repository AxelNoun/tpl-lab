"""Upgrade #6 — power analysis BEFORE touching real data.

Question: with n samples in intrinsic dimension d, can our pipeline tell
S^d from T^d at all? Two probes: (a) topological (does betti1 find the torus
loops?), (b) fingerprint ranking (is the true generator ranked first?).
First finding (kept in docs/RESULTATS_NEGATIFS.md): direct b1 detection dies
by d ~ 4 at n <= 3000 — real protocols must rely on ranking/contrast, or on
circular-coordinate methods, or on far larger n.
Run a fuller grid: python -m tpl.analysis.calibration --full
"""
import argparse
import numpy as np

from tpl.analysis.topology import betti1
from tpl.analysis.model_comparison import rank_candidates
from tpl.generative.manifolds import sphere, torus_flat


def topo_power(dim, n, n_rep=3, seed=0):
    hits = sum(betti1(torus_flat(n, dim=dim, noise=0.02, seed=seed + r),
                      dim=dim, seed=seed + r) >= 1 for r in range(n_rep))
    fps = sum(betti1(sphere(n, dim=dim, noise=0.02, seed=seed + 50 + r),
                     dim=dim, seed=seed + r) >= 1 for r in range(n_rep))
    return hits / n_rep, fps / n_rep


def ranking_power(dim, n, n_rep=3, seed=0):
    cands = {"S6": lambda **k: sphere(dim=dim, **k),
             "T6": lambda **k: torus_flat(dim=dim, **k)}
    ok = 0
    for r in range(n_rep):
        data = torus_flat(n, dim=dim, noise=0.05, seed=seed + 200 + r)
        ok += next(iter(rank_candidates(data, n_boot=2, seed=seed + r,
                                        candidates=cands))) == "T6"
    return ok / n_rep


def run(dims=(2, 3), n=1500, n_rep=2, seed=0):
    print(f"{'d':>2} {'topo TPR':>9} {'topo FPR':>9} {'rank acc':>9}   (n={n})")
    for d in dims:
        tpr, fpr = topo_power(d, n, n_rep, seed)
        acc = ranking_power(d, n, n_rep, seed)
        print(f"{d:>2} {tpr:>9.2f} {fpr:>9.2f} {acc:>9.2f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    run(dims=(2, 3, 4, 6) if a.full else (2, 3),
        n=3000 if a.full else 1500, n_rep=3 if a.full else 2, seed=a.seed)
