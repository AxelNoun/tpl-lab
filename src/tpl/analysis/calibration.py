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
from tpl.analysis.model_comparison import rank_candidates, MAX_FIT_SCORE
from tpl.generative.manifolds import sphere, torus_flat, euclidean
from tpl.nulls.kuramoto import simulate_kuramoto


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


def _nonuniform_sphere(n, dim=6, noise=0.03, seed=0, kappa=2.0):
    """Same manifold, deliberately non-uniform density: real sampling never is."""
    rng = np.random.default_rng(seed)
    out, got = [], 0
    while got < n:
        x = rng.standard_normal((4 * n, dim + 1))
        x /= np.linalg.norm(x, axis=1, keepdims=True)
        x = x[rng.random(len(x)) < np.exp(kappa * x[:, 0]) / np.exp(kappa)]
        out.append(x)
        got += len(x)
    x = np.concatenate(out)[:n]
    return x + noise * rng.standard_normal(x.shape)


def _kuramoto_cloud(n, seed=0, K=2.0):
    """The project's own null, embedded as a point cloud and decorrelated."""
    return np.sin(simulate_kuramoto(n=12, K=K, n_steps=n * 4, seed=seed))[::4][:n]


def fit_threshold(n=2000, n_rep=4, seed=0):
    """Calibrate the absolute goodness-of-fit cutoff MAX_FIT_SCORE.

    Positives are data that genuinely IS one of the candidates (including noisy
    and non-uniform variants); negatives are data that is none of them, plus the
    Kuramoto null. A usable threshold needs the two classes to separate.
    """
    positive = [
        ("S6 bruit 0.03", lambda s: sphere(n, dim=6, noise=0.03, seed=s)),
        ("S6 bruit 0.10", lambda s: sphere(n, dim=6, noise=0.10, seed=s)),
        ("S6 non uniforme", lambda s: _nonuniform_sphere(n, seed=s)),
        ("T6 bruit 0.03", lambda s: torus_flat(n, dim=6, noise=0.03, seed=s)),
        ("R6 bruit 0.03", lambda s: euclidean(n, dim=6, noise=0.03, seed=s)),
    ]
    negative = [
        ("S3", lambda s: sphere(n, dim=3, noise=0.03, seed=s)),
        ("S10", lambda s: sphere(n, dim=10, noise=0.03, seed=s)),
        ("T3", lambda s: torus_flat(n, dim=3, noise=0.03, seed=s)),
        ("gaussienne 20-D", lambda s: np.random.default_rng(s).standard_normal((n, 20)) / np.sqrt(20)),
        ("Kuramoto K=0", lambda s: _kuramoto_cloud(n, seed=s, K=0.0)),
        ("Kuramoto K=2", lambda s: _kuramoto_cloud(n, seed=s, K=2.0)),
    ]
    print(f"seuil courant MAX_FIT_SCORE = {MAX_FIT_SCORE}  (n={n}, {n_rep} graines)")
    out = {}
    for label, cases in (("VRAIE geometrie candidate", positive), ("AUCUNE", negative)):
        print(f"\n--- {label} ---")
        vals = []
        for name, gen in cases:
            s = [min(rank_candidates(gen(seed + r), seed=seed + r).values()) for r in range(n_rep)]
            vals += s
            print(f"  {name:<18s} min={min(s):6.2f} max={max(s):6.2f}")
        out[label] = np.array(vals)
    pos, neg = out["VRAIE geometrie candidate"], out["AUCUNE"]
    print(f"\nmarge de separation : [{pos.max():.2f} , {neg.min():.2f}]  "
          f"seuil retenu {MAX_FIT_SCORE}")
    print(f"  faux positifs (accepte a tort) : {100 * (neg <= MAX_FIT_SCORE).mean():.0f}%")
    print(f"  faux negatifs (rejete a tort)  : {100 * (pos > MAX_FIT_SCORE).mean():.0f}%")


def run(dims=(2, 3), n=1500, n_rep=2, seed=0):
    print(f"{'d':>2} {'topo TPR':>9} {'topo FPR':>9} {'rank acc':>9}   (n={n})")
    for d in dims:
        tpr, fpr = topo_power(d, n, n_rep, seed)
        acc = ranking_power(d, n, n_rep, seed)
        print(f"{d:>2} {tpr:>9.2f} {fpr:>9.2f} {acc:>9.2f}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--fit-threshold", action="store_true",
                    help="recalibrate the absolute goodness-of-fit cutoff")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    if a.fit_threshold:
        fit_threshold(seed=a.seed)
    else:
        run(dims=(2, 3, 4, 6) if a.full else (2, 3),
            n=3000 if a.full else 1500, n_rep=3 if a.full else 2, seed=a.seed)
