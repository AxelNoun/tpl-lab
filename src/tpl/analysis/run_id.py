"""Chantier 7 — the preregistered pipeline, as a single frozen entry point.

    python -m tpl.analysis.run_id --config configs/prereg_v1.json --data X.npy
    python -m tpl.analysis.run_id --config configs/prereg_v1.json --synthetic

PREREGISTRATION.md names this command; until audit v2 it did not exist, so the
prereg described an analysis nobody could re-run (docs/RESULTATS_NEGATIFS.md,
F4). Every parameter comes from the config file and is echoed in the output:
this module chooses nothing. Its whole job is to make the choices auditable and
to refuse to answer when the data cannot support an answer.

`--data` expects a .npy array (n_windows, n_channels) of population vectors,
already cut into the non-overlapping windows the config declares. Decimation to
independence is applied HERE, not by the caller.
"""
import argparse
import json
from pathlib import Path

import numpy as np

from tpl.analysis.bridge import prepare_population
from tpl.analysis.intrinsic_dim import decorrelate, max_lag_for, twonn
from tpl.analysis.model_comparison import select_geometry
from tpl.analysis.state_contrast import contrast


def load_config(path):
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    if cfg["geometry"]["max_fit_score"] != 3.0:
        raise ValueError("max_fit_score is calibrated in docs/09; changing it "
                         "post hoc is exactly the HARKing the prereg forbids")
    if cfg.get("bridge", {}).get("reduce_to_r7", False):
        raise ValueError("reduce_to_r7 is the degree of freedom docs/02 exists "
                         "to forbid; turning it on after seeing data is HARKing")
    return cfg


def classify_id(value, targets, tolerance):
    """The pre-registered verdict on the intrinsic dimension.

    Acceptance windows are half-open, [t - tol, t + tol), and the refutation
    zones fill every remaining value. Audit v2 (F7) found the prose version was
    neither exhaustive (ID < 5.5 fell through) nor disjoint (6.5 and 7.5 each
    sat in an acceptance AND a refutation interval). Half-open windows are never
    more permissive than the original wording at any point.
    """
    ts = sorted(targets)
    lo = ts[0] - tolerance
    if value < lo:
        return "refutee", f"ID = {value:.2f} < {lo:g} : variete de dimension plus basse que predit"
    for i, t in enumerate(ts):
        if value < t + tolerance:
            if value < t - tolerance:
                return "refutee", (f"ID = {value:.2f} dans [{ts[i-1] + tolerance:g}, "
                                   f"{t - tolerance:g}[ : entre deux entiers predits")
            return "compatible", (f"ID = {value:.2f} dans [{t - tolerance:g}, "
                                  f"{t + tolerance:g}[ : compatible avec d = {t}")
    hi = ts[-1] + tolerance
    return "refutee", f"ID = {value:.2f} >= {hi:g} : variete de dimension plus haute que predit"


def run_condition(points, cfg, label="A"):
    """Decimate, then apply the two primary measures — or decline to conclude.

    A verdict is withheld when decorrelation leaves too few samples. TwoNN
    approaches d from below, so a short recording refutes a CORRECT hypothesis:
    on a true S6, the false-refutation rate is 14% at n = 1000 and 1% at
    n = 2000. Reporting 'insufficient' is the only honest output there.
    """
    idc = cfg["intrinsic_dimension"]
    points = prepare_population(points)
    thinned, lag = decorrelate(points, threshold=cfg["decimation"]["threshold"])
    out = {"label": label, "n_raw": len(points), "lag": lag, "n": len(thinned),
           "n_min": idc["min_samples_after_decimation"], "points": thinned}

    # Hitting the cap means the series never decorrelated, so the surviving
    # samples are not independent and TwoNN stays biased low on them. A chaotic
    # RNN at g = 1.8 reached the cap and returned a plausible d = 6.14 on 140
    # still-correlated samples — which would have read as a confirmation.
    if lag >= max_lag_for(len(points)):
        out["verdict"] = "indecidable"
        out["reason"] = (f"autocorrelation jamais descendue sous "
                         f"{cfg['decimation']['threshold']} en {lag} pas : la serie "
                         f"n'est pas decorrelable a cette longueur")
        return out

    if len(thinned) < idc["min_samples_after_decimation"]:
        out["verdict"] = "indecidable"
        out["reason"] = (f"{len(thinned)} echantillons independants < "
                         f"{idc['min_samples_after_decimation']} requis : puissance "
                         f"insuffisante, aucune conclusion (ni pour, ni contre)")
        return out

    out["id"] = twonn(thinned)
    out["id_verdict"], out["reason"] = classify_id(out["id"], idc["targets"], idc["tolerance"])
    sel = select_geometry(thinned, seed=cfg["seed"])
    out["geometry"], out["best_candidate"] = sel["geometry"], sel["best_candidate"]
    out["fit_score"], out["ranking"] = sel["score"], sel["ranking"]

    # H1 needs BOTH primary measures, because measure 1 alone does not beat the
    # nulls: allowing the d = 8 variant makes the acceptance window wide enough
    # that a 12-oscillator Kuramoto network lands in it (ID = 8.23) while fitting
    # no candidate geometry at all (best score 55.8 vs 0.47 for a true S6).
    if out["id_verdict"] == "refutee":
        out["verdict"] = "refutee"
    elif out["geometry"] is None:
        out["verdict"] = "refutee"
    else:
        out["verdict"] = "compatible"
    return out


def _format(res, cfg):
    lines = [f"  [{res['label']}] {res['n_raw']} fenetres -> decimation 1/{res['lag']} "
             f"-> {res['n']} echantillons independants (minimum {res['n_min']})"]
    if res["verdict"] == "indecidable":
        lines.append(f"      INDECIDABLE : {res['reason']}")
        return lines
    lines.append(f"      mesure 1 (dimension)  : {res['reason']}  -> {res['id_verdict']}")
    if res["geometry"] is None:
        geom = (f"AUCUNE : meilleur candidat {res['best_candidate']}, score "
                f"{res['fit_score']:.2f} > {cfg['geometry']['max_fit_score']}  -> refutee")
    else:
        geom = f"{res['geometry']} (score {res['fit_score']:.2f})  -> compatible"
    lines.append(f"      mesure 2 (geometrie)  : {geom}")
    lines.append(f"      verdict H1 (les deux) : {res['verdict'].upper()}")
    return lines


def main(argv=None):
    p = argparse.ArgumentParser(description="Preregistered intrinsic-dimension pipeline")
    p.add_argument("--config", default="configs/prereg_v1.json")
    p.add_argument("--data", help=".npy of shape (n_windows, n_channels)")
    p.add_argument("--data-b", help="second condition, enables the contrast")
    p.add_argument("--synthetic", action="store_true",
                   help="dry-run the frozen pipeline on synthetic data (synth_ outputs)")
    p.add_argument("--seed", type=int, default=None, help="overrides the config seed")
    a = p.parse_args(argv)

    cfg = load_config(a.config)
    if a.seed is not None:
        cfg["seed"] = a.seed
    print(f"config {a.config} | seed {cfg['seed']} | fenetres "
          f"{cfg['windows']['length_ms']} ms non chevauchantes | "
          f"decimation jusqu'a autocorrelation < {cfg['decimation']['threshold']}")

    if a.synthetic:
        from tpl.generative.s6_flow import simulate_su3_flow
        from tpl.nulls.kuramoto import simulate_kuramoto
        print("!! DONNEES SYNTHETIQUES (synth_) — dry-run du pipeline, "
              "aucune valeur empirique !!")
        cond = [("synth_flot_su3", simulate_su3_flow(n_steps=70000, noise=1.2, seed=cfg["seed"])),
                ("synth_nul_kuramoto", np.sin(simulate_kuramoto(n=12, n_steps=70000,
                                                                seed=cfg["seed"])))]
    elif a.data:
        cond = [("A", np.load(a.data))]
        if a.data_b:
            cond.append(("B", np.load(a.data_b)))
    else:
        p.error("give --data or --synthetic")

    results = [run_condition(pts, cfg, label) for label, pts in cond]
    for res in results:
        print("\n".join(_format(res, cfg)))

    if len(results) == 2 and all(r["verdict"] != "indecidable" for r in results):
        c = contrast(results[0]["points"], results[1]["points"],
                     n_boot=cfg["contrast"]["n_boot"],
                     frac=cfg["contrast"]["subsample_frac"], seed=cfg["seed"])
        lo, hi = c["delta_id_ci95"]
        sig = "exclut 0" if lo > 0 or hi < 0 else "inclut 0 (pas de difference)"
        print(f"\n  contraste : delta ID = {c['delta_id']:.2f}  CI95 [{lo:.2f}, {hi:.2f}] -> {sig}")
    return results


if __name__ == "__main__":
    main()
