"""End-to-end synthetic demo. Run: python -m tpl.demo --seed 42
Covers upgrades 1-6. Everything here is SYNTHETIC (rule 3, CLAUDE.md)."""
import argparse
import numpy as np

from tpl.generative.s6_flow import simulate_su3_flow, observe, sample_s6_uniform
from tpl.generative.manifolds import sphere, torus_flat, euclidean
from tpl.nulls.kuramoto import simulate_kuramoto, order_parameter
from tpl.analysis.intrinsic_dim import twonn
from tpl.analysis.triplet_phase import closure_naive, closure_windowed
from tpl.analysis.topology import betti1
from tpl.analysis.model_comparison import rank_candidates, select_geometry, MAX_FIT_SCORE
from tpl.analysis.spectral import covariance_spectrum, matches_s6_profile
from tpl.analysis.state_contrast import contrast


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()
    s = args.seed
    print(f"[seed={s}]  SYNTHETIC DATA ONLY\n")

    print("— [6] Dimension intrinsèque (TwoNN) —")
    print(f"  S^6 i.i.d. (vrai 6) : d = {twonn(sample_s6_uniform(4000, seed=s)):.2f}")
    print(f"  Gaussienne 8D (vrai 8) : d = {twonn(np.random.default_rng(s).standard_normal((4000, 8))):.2f}")
    flow = simulate_su3_flow(n_steps=20000, noise=1.2, seed=s)
    print(f"  Flot su(3) réel (g2 octonionique), décimé : d = {twonn(flow[::10]):.2f}")

    print("\n— [1] Topologie : sphère vs tore (b1, critère de gap) —")
    print(f"  b1(S^2) = {betti1(sphere(2000, dim=2, noise=0.02, seed=s), seed=s)}   "
          f"b1(T^2) = {betti1(torus_flat(2000, dim=2, noise=0.02, seed=s), seed=s)}  (vrai : 0 / 2)")
    print("  d=6 : puissance nulle à ce n -> b1=0 partout, voir calibration (module 6).")

    print("\n— [2,4] Comparaison de géométries candidates (score : plus petit = mieux) —")
    for name, gen in [("données S6", sphere), ("données T6", torus_flat)]:
        r = rank_candidates(gen(2000, dim=6, noise=0.03, seed=s), seed=s)
        best = next(iter(r))
        print(f"  {name} -> gagnant {best}  {dict((k, round(v, 2)) for k, v in r.items())}")
    print(f"  seuil d'adéquation absolu = {MAX_FIT_SCORE} (calibré : "
          f"python -m tpl.analysis.calibration --fit-threshold)")
    for name, data in [("données S6", sphere(2000, dim=6, noise=0.03, seed=s)),
                       ("données S3 (aucun candidat)", sphere(2000, dim=3, noise=0.03, seed=s)),
                       ("bruit 20-D (aucun candidat)",
                        np.random.default_rng(s).standard_normal((2000, 20)) / np.sqrt(20))]:
        sel = select_geometry(data, seed=s)
        verdict = sel["geometry"] or f"AUCUN (meilleur : {sel['best_candidate']})"
        print(f"  {name:<28s} -> {verdict}  score {sel['score']:.2f}")

    print("\n— [5] Spectre G2 : prédiction exacte à 4 niveaux (corrigée par audit v1) —")
    ev = covariance_spectrum(sphere(20000, dim=6, seed=s))
    print(f"  théorie 1/7 | 2/63 | 1/63 | 0  x(7|6|21|1) — la '27' de G2 scindée 6+21 en base brute")
    print(f"  observé {ev[:7].mean():.4f} | {ev[7:13].mean():.4f} | {ev[13:34].mean():.4f} | {ev[34]:.1e}"
          f"   match S6 : {matches_s6_profile(ev)}")
    g7 = np.random.default_rng(s).standard_normal((20000, 7)) / np.sqrt(7)
    print(f"  gaussienne 7D : match S6 = {matches_s6_profile(covariance_spectrum(g7))}")

    print("\n— [3] Contraste d'états (simulé : 'veille' S^6 vs 'anesthésie' effondrée) —")
    c = contrast(sphere(1500, dim=6, noise=0.02, seed=s), euclidean(1500, dim=3, noise=0.02, seed=s), seed=s)
    print(f"  delta ID = {c['delta_id']:.2f}  CI95 {tuple(round(x, 2) for x in c['delta_id_ci95'])} "
          f"(sous-échantillonnage sans remise, n_boot={c['n_boot']})")
    print(f"  veille     -> géométrie {c['A']['best_geometry']} (score {c['A']['fit_score']:.2f})")
    print(f"  anesthésie -> géométrie {c['B']['best_geometry']} "
          f"(meilleur candidat {c['B']['best_candidate']}, score {c['B']['fit_score']:.2f} "
          f"> {MAX_FIT_SCORE} : aucun ne convient)")

    print("\n— Rappel (docs/03) : la 'signature' de l'article source est morte —")
    th = simulate_kuramoto(seed=s)
    sig = np.sin(th[:, :3])
    print(f"  Kuramoto r = {order_parameter(th):.2f} ; closure naïve = {closure_naive(sig):.1e} (tautologie) ;"
          f" fenêtrée = {closure_windowed(sig):.3f} rad (le nul la satisfait)")

    print("\nCalibration complète : python -m tpl.analysis.calibration --full")


if __name__ == "__main__":
    main()
