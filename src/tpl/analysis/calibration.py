"""Upgrade #6 — power analysis BEFORE touching real data.

Question: with n samples in intrinsic dimension d, can our pipeline tell
S^d from T^d at all? Two probes: (a) topological (does betti1 find the torus
loops?), (b) fingerprint ranking (is the true generator ranked first?).
First finding (kept in docs/RESULTATS_NEGATIFS.md): direct b1 detection dies
by d = 3 at n <= 3000 (this docstring said d ~ 4 until audit v2 measured it:
T^3 scored 0 detections out of 30 at n = 2000, while docs/12 had it right) —
real protocols must rely on ranking/contrast, or on circular-coordinate
methods, or on far larger n.
Run a fuller grid: python -m tpl.analysis.calibration --full
"""
import argparse
import numpy as np

from tpl.analysis.topology import betti1
from tpl.analysis.intrinsic_dim import twonn
from tpl.analysis.model_comparison import rank_candidates, select_geometry, MAX_FIT_SCORE
from tpl.analysis.run_id import classify_id, h1_verdict
from tpl.generative.manifolds import sphere, torus_flat, euclidean
from tpl.nulls.kuramoto import simulate_kuramoto


def topo_power(dim, n, n_rep=3, seed=0):
    hits = sum(betti1(torus_flat(n, dim=dim, noise=0.02, seed=seed + r),
                      dim=dim, seed=seed + r) >= 1 for r in range(n_rep))
    fps = sum(betti1(sphere(n, dim=dim, noise=0.02, seed=seed + 50 + r),
                     dim=dim, seed=seed + r) >= 1 for r in range(n_rep))
    return hits / n_rep, fps / n_rep


def ranking_power(dim, n, n_rep=3, seed=0):
    """Candidates are labelled by the dimension actually being swept: this used
    to hardcode 'S6'/'T6' and so reported 'S6' for a 2-sphere (audit v2, F14)."""
    sphere_name, torus_name = f"S{dim}", f"T{dim}"
    cands = {sphere_name: lambda **k: sphere(dim=dim, **k),
             torus_name: lambda **k: torus_flat(dim=dim, **k)}
    ok = 0
    for r in range(n_rep):
        data = torus_flat(n, dim=dim, noise=0.05, seed=seed + 200 + r)
        ok += next(iter(rank_candidates(data, n_boot=2, seed=seed + r,
                                        candidates=cands))) == torus_name
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


def _ci_variants(pts_a, pts_b, n_boot, frac, seed):
    """The two candidate intervals, computed from ONE set of subsamples so the
    comparison is not confounded by resampling noise."""
    rng = np.random.default_rng(seed)
    theta = twonn(pts_a) - twonn(pts_b)
    ma, mb = int(len(pts_a) * frac), int(len(pts_b) * frac)
    diffs = np.empty(n_boot)
    for k in range(n_boot):
        diffs[k] = (twonn(pts_a[rng.choice(len(pts_a), ma, replace=False)])
                    - twonn(pts_b[rng.choice(len(pts_b), mb, replace=False)]))
    naive = tuple(np.percentile(diffs, [2.5, 97.5]))
    rate = np.sqrt(0.5 * (ma / len(pts_a) + mb / len(pts_b)))
    q_lo, q_hi = np.percentile(diffs - theta, [2.5, 97.5])
    return theta, naive, (theta - rate * q_hi, theta - rate * q_lo)


def ci_coverage(n=1200, n_rep=60, n_boot=300, frac=0.632, seed=0, dims=(6, 3)):
    """Does the delta-ID interval actually cover the TRUE difference 95% of the time?

    The prereg's primary measure 2 reads 'CI95 excluding 0', so the interval has
    to mean what it says. Ground truth is known here by construction: S^dims[0]
    against S^dims[1]. Compares the naive percentile interval against the
    subsampling construction now used in state_contrast.contrast.
    """
    truth = dims[0] - dims[1]
    print(f"vraie difference = {truth}  (S^{dims[0]} vs S^{dims[1]}, n={n}, "
          f"{n_rep} repetitions, n_boot={n_boot})")
    hits = {"naif": 0, "sous-echantillonnage": 0}
    widths = {"naif": [], "sous-echantillonnage": []}
    off_centre = 0
    for r in range(n_rep):
        a = sphere(n, dim=dims[0], noise=0.02, seed=seed + 900 + r)
        b = sphere(n, dim=dims[1], noise=0.02, seed=seed + 400 + r)
        theta, naive, sub = _ci_variants(a, b, n_boot, frac, seed + r)
        off_centre += not (naive[0] <= theta <= naive[1])
        for name, (lo, hi) in (("naif", naive), ("sous-echantillonnage", sub)):
            hits[name] += lo <= truth <= hi
            widths[name].append(hi - lo)
    print(f"\n  {'intervalle':<22s} {'couverture':>11s} {'largeur moy.':>13s}")
    for name in hits:
        print(f"  {name:<22s} {100 * hits[name] / n_rep:>10.0f}% "
              f"{np.mean(widths[name]):>13.2f}")
    print(f"\n  l'intervalle naif excluait sa propre estimation ponctuelle dans "
          f"{100 * off_centre / n_rep:.0f}% des cas")


def _one_h1(points, seed):
    d = twonn(points)
    id_v, _ = classify_id(d, [6, 8], 0.5)
    sel = select_geometry(points, seed=seed, n_boot=2)
    return h1_verdict(id_v, sel["geometry"]), id_v, sel["geometry"]


def h1_power(n=2000, n_rep=8, seed=0):
    """TPR / FPR of the conjunctive H-TPL rule at one n."""
    gens = [
        ("S6 (doit accepter)", lambda s: sphere(n, dim=6, noise=0.03, seed=s), "compatible"),
        ("T6 (rival, doit refuter)", lambda s: torus_flat(n, dim=6, noise=0.03, seed=s), "refutee"),
        ("R6 (rival, doit refuter)", lambda s: euclidean(n, dim=6, noise=0.03, seed=s), "refutee"),
        ("Kuramoto K=2", lambda s: _kuramoto_cloud(n, seed=s, K=2.0), "refutee"),
        ("gaussienne 20-D", lambda s: np.random.default_rng(s).standard_normal((n, 20)) / np.sqrt(20), "refutee"),
    ]
    print(f"verdict H-TPL = dimension compatible ET geometrie S6   "
          f"(n={n}, {n_rep} graines, select_geometry n_boot=2)")
    print(f"  {'donnees':<28s} {'attendu':>10s} {'TPR/TNR':>8s}  "
          f"{'ID ok':>6s} {'S6':>5s} {'T6':>5s} {'aucun':>6s}")
    summary = {}
    for name, gen, expected in gens:
        hits = id_ok = s6 = t6 = none = 0
        for r in range(n_rep):
            v, id_v, geom = _one_h1(gen(seed + r), seed + r)
            hits += v == expected
            id_ok += id_v == "compatible"
            s6 += geom == "S6"
            t6 += geom == "T6"
            none += geom is None
        rate = 100 * hits / n_rep
        summary[name] = {"rate": rate, "id_ok": 100 * id_ok / n_rep,
                         "s6": 100 * s6 / n_rep, "t6": 100 * t6 / n_rep,
                         "none": 100 * none / n_rep}
        print(f"  {name:<28s} {expected:>10s} {rate:7.0f}%  "
              f"{summary[name]['id_ok']:5.0f}% {summary[name]['s6']:4.0f}% "
              f"{summary[name]['t6']:4.0f}% {summary[name]['none']:5.0f}%")
    return summary


def h1_power_curve(ns=(500, 1000, 1500, 2000), n_rep=8, seed=0):
    """Does the n_min = 2000 floor sit where TPR actually recovers?

    Below the floor the pipeline returns INDECIDABLE; this curve is the
    underlying rule, un-gated, so the floor can be compared to measured power
    rather than to a guess.
    """
    rows = {}
    for n in ns:
        print(f"\n===== n = {n} =====")
        rows[n] = h1_power(n=n, n_rep=n_rep, seed=seed)
    print(f"\nTPR(n) sur un vrai S6  (pipeline sans le plancher n_min) :")
    print(f"  {'n':>6s} {'TPR H-TPL':>10s} {'ID ok':>8s} {'S6':>8s}")
    for n, s in rows.items():
        u = s["S6 (doit accepter)"]
        print(f"  {n:6d} {u['rate']:9.0f}% {u['id_ok']:7.0f}% {u['s6']:7.0f}%")
    return rows


def h1_noise(n=2000, n_rep=8, noises=(0.03, 0.08, 0.12, 0.15, 0.20), seed=0):
    """Power vs additive noise on a true S6, at the prereg n.

    MAX_FIT_SCORE was calibrated to reject a genuine S6 at noise >= 0.15
    (docs/09). This re-measures that limit on the named conjunctive verdict,
    not on the ranking score alone.
    """
    print(f"vrai S6, n={n}, {n_rep} graines : TPR en fonction du bruit additif")
    print(f"  {'bruit':>6s} {'TPR H-TPL':>10s} {'ID ok':>8s} {'S6 accepte':>12s} {'aucun':>8s}")
    out = {}
    for noise in noises:
        hits = id_ok = s6 = none = 0
        for r in range(n_rep):
            v, id_v, geom = _one_h1(sphere(n, dim=6, noise=noise, seed=seed + r), seed + r)
            hits += v == "compatible"
            id_ok += id_v == "compatible"
            s6 += geom == "S6"
            none += geom is None
        out[noise] = (100 * hits / n_rep, 100 * id_ok / n_rep,
                      100 * s6 / n_rep, 100 * none / n_rep)
        h, i, g, z = out[noise]
        print(f"  {noise:6.2f} {h:9.0f}% {i:7.0f}% {g:11.0f}% {z:7.0f}%")
    return out


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
    ap.add_argument("--ci-coverage", action="store_true",
                    help="measure the coverage of the delta-ID interval")
    ap.add_argument("--h1-power", action="store_true",
                    help="TPR/FPR of the conjunctive H-TPL verdict (curve over n)")
    ap.add_argument("--h1-noise", action="store_true",
                    help="TPR of a true S6 vs additive noise")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    if a.fit_threshold:
        fit_threshold(seed=a.seed)
    elif a.ci_coverage:
        ci_coverage(seed=a.seed)
    elif a.h1_power:
        h1_power_curve(seed=a.seed)
    elif a.h1_noise:
        h1_noise(seed=a.seed)
    else:
        run(dims=(2, 3, 4, 6) if a.full else (2, 3),
            n=3000 if a.full else 1500, n_rep=3 if a.full else 2, seed=a.seed)
