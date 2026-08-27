"""Chantier 8 analysis: MDS of a similarity matrix, then rival geometries.

This does NOT restore H1. Neural S6 on public Neuropixels is already
refuted; a perceptual sphere would be a different claim (docs/08).
CIELAB-like Euclidean colour is the strong null.
"""

import numpy as np

from tpl.analysis.manifold_evidence import _mds
from tpl.analysis.model_comparison import select_geometry
from tpl.generative.manifolds import euclidean, sphere


def dissimilarity_from_ratings(ratings):
    """ratings (n_stim, n_stim) higher = more similar → distance."""
    r = np.asarray(ratings, float)
    r = 0.5 * (r + r.T)
    d = r.max() - r
    np.fill_diagonal(d, 0.0)
    return np.maximum(d, 0.0)


def embed(dissimilarity, dim=3):
    return _mds(np.asarray(dissimilarity, float), dim)


def stress(dissimilarity, coords):
    d = np.asarray(dissimilarity, float)
    hat = np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=-1)
    iu = np.triu_indices_from(d, k=1)
    num = np.sum((d[iu] - hat[iu]) ** 2)
    den = np.sum(d[iu] ** 2)
    return float(np.sqrt(num / max(den, 1e-12)))


def rival_fit(dissimilarity, seed=0):
    """Stress of 3-D MDS vs unit-sphere projection vs the neural ranking.

    Colour psychophysics is 2–3 D, not S6. select_geometry on 12 points is
    underpowered and is stored only as a secondary label.
    """
    coords = embed(dissimilarity, dim=3)
    nrm = np.linalg.norm(coords, axis=1, keepdims=True)
    sphere = coords / np.maximum(nrm, 1e-12)
    out = {
        "stress_euclidean": stress(dissimilarity, coords),
        "stress_sphere": stress(dissimilarity, sphere),
        "n_stim": int(len(coords)),
    }
    if len(coords) >= 20:
        sel = select_geometry(coords, seed=seed, n_boot=2)
        out["geometry"] = sel["geometry"]
        out["fit_score"] = sel["score"]
    return out


def _format(fit, label):
    lines = [
        f"  [{label}] n_stim={fit['n_stim']}  "
        f"stress euclidien={fit['stress_euclidean']:.4f}  "
        f"sphere={fit['stress_sphere']:.4f}"
    ]
    if fit["stress_euclidean"] <= fit["stress_sphere"]:
        lines.append("      nul euclidien / CIELAB-like gagne ou egale (H8-0)")
    else:
        lines.append("      sphere gagne le stress (H8-sphere) — ne restaure pas H1")
    if "geometry" in fit:
        geom = fit["geometry"] or "aucune"
        lines.append(
            f"      select_geometry secondaire : {geom}  "
            f"score {fit['fit_score']:.2f}  (pas H8, pas H1)"
        )
    return "\n".join(lines)


def synthetic_dissimilarity(kind, n=24, seed=0):
    """kind 'sphere' = S^2 chordal; 'euclidean' = R^3. Both synth_."""
    rng_kind = kind
    if rng_kind == "sphere":
        pts = sphere(n, dim=2, noise=0.0, seed=seed)
    elif rng_kind == "euclidean":
        pts = euclidean(n, dim=3, noise=0.02, seed=seed)
    else:
        raise ValueError("kind must be 'sphere' or 'euclidean'")
    return np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=-1)


def main(argv=None):
    import argparse

    p = argparse.ArgumentParser(
        description="Chantier 8: sphere vs Euclidean stress (not H1)"
    )
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--synthetic",
        action="store_true",
        help="dry-run on synth_ dissimilarities (sphere chordal + Euclidean)",
    )
    p.add_argument(
        "--ratings",
        help="(n_stim, n_stim) .npy of similarity ratings (higher = more similar)",
    )
    a = p.parse_args(argv)
    print(f"[seed={a.seed}]  chantier 8  (ne restaure pas H1)")
    if a.synthetic:
        print("!! DONNEES SYNTHETIQUES (synth_) — pas des jugements humains !!")
        for kind in ("sphere", "euclidean"):
            d = synthetic_dissimilarity(kind, n=24, seed=a.seed)
            fit = rival_fit(d, seed=a.seed)
            print(_format(fit, f"synth_{kind}"))
        return 0
    if a.ratings:
        ratings = np.load(a.ratings)
        d = dissimilarity_from_ratings(ratings)
        print(_format(rival_fit(d, seed=a.seed), a.ratings))
        return 0
    p.error("give --synthetic or --ratings")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
