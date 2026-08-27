"""Secondary manifold evidence: a geodesic-kernel GP, not the frozen H1.

This is the numpy stand-in for mGPLVM (Jensen et al. 2020) documented in
docs/09. It does NOT replace `select_geometry` and does not retune
MAX_FIT_SCORE. Latents are a frozen classical MDS of a subsample, projected
onto S6 / T6 / R6; only the kernel lengthscale is grid-searched.

A higher log-likelihood is better. `select_evidence` names a winner only as
a ranking — H1 still requires `select_geometry` + TwoNN.
"""

import numpy as np

from tpl.analysis.topology import rescale_to_unit


def _mds(distances, dim):
    d = np.asarray(distances, float)
    n = d.shape[0]
    j = np.eye(n) - np.ones((n, n)) / n
    b = -0.5 * j @ (d**2) @ j
    vals, vecs = np.linalg.eigh(b)
    order = np.argsort(vals)[::-1][:dim]
    w = np.maximum(vals[order], 0.0)
    return vecs[:, order] * np.sqrt(w)


def _pairwise(pts):
    return np.linalg.norm(pts[:, None, :] - pts[None, :, :], axis=-1)


def _sphere_latents(embed7):
    nrm = np.linalg.norm(embed7, axis=1, keepdims=True)
    nrm = np.maximum(nrm, 1e-12)
    return embed7 / nrm


def _torus_latents(embed12):
    """Recover 6 angles from a 12-D MDS cloud that may have been rotated."""
    z = np.asarray(embed12, float)
    remaining = list(range(z.shape[1]))
    angles = []
    while len(remaining) >= 2:
        best_pair, best_score = None, np.inf
        for i, a in enumerate(remaining):
            for b in remaining[i + 1 :]:
                r = np.sqrt(z[:, a] ** 2 + z[:, b] ** 2)
                score = float(r.std() / (r.mean() + 1e-12))
                if score < best_score:
                    best_score = score
                    best_pair = (a, b)
        a, b = best_pair
        angles.append(np.arctan2(z[:, b], z[:, a]))
        remaining.remove(a)
        remaining.remove(b)
    return np.stack(angles, axis=1)


def _geodesic(latents, kind):
    if kind == "S6":
        g = np.clip(latents @ latents.T, -1.0, 1.0)
        return np.arccos(g)
    if kind == "T6":
        d = latents[:, None, :] - latents[None, :, :]
        d = (d + np.pi) % (2 * np.pi) - np.pi
        return np.sqrt(np.sum(d**2, axis=-1))
    return _pairwise(latents)


def _rbf(geo, lengthscale):
    return np.exp(-0.5 * (geo / lengthscale) ** 2)


def _gp_loglik(y, kernel, noise=1e-2):
    n = len(y)
    k = 0.5 * (kernel + kernel.T)
    k = k + noise * np.eye(n)
    vals, vecs = np.linalg.eigh(k)
    vals = np.maximum(vals, 1e-8)
    inv_y = vecs @ ((vecs.T @ y) / vals)
    return float(
        -0.5 * y @ inv_y - 0.5 * np.log(vals).sum() - 0.5 * n * np.log(2 * np.pi)
    )


def evidence(pts, seed=0, n_sub=300):
    """Log GP evidence for S6, T6, R6 on one random readout of a subsample."""
    rng = np.random.default_rng(seed)
    pts = rescale_to_unit(np.asarray(pts, float))
    if len(pts) > n_sub:
        pts = pts[rng.choice(len(pts), n_sub, replace=False)]
    w = rng.standard_normal(pts.shape[1])
    w /= np.linalg.norm(w)
    y = pts @ w
    y = y - y.mean()
    d = _pairwise(pts)
    z_s = _sphere_latents(_mds(d, 7))
    z_t = _torus_latents(_mds(d, 12))
    z_r = _mds(d, 6)
    out = {}
    for name, z, kind in (("S6", z_s, "S6"), ("T6", z_t, "T6"), ("R6", z_r, "R6")):
        geo = _geodesic(z, kind)
        med = float(np.median(geo[np.triu_indices_from(geo, k=1)]))
        med = max(med, 1e-3)
        scores = []
        for ell in (0.3, 0.6, 1.0, 1.5, 2.5, 4.0):
            scores.append(_gp_loglik(y, _rbf(geo, ell * med)))
        out[name] = float(max(scores))
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def select_evidence(pts, seed=0, n_sub=300):
    """Ranking only. Not an H1 verdict."""
    ev = evidence(pts, seed=seed, n_sub=n_sub)
    best = next(iter(ev))
    return {"geometry": best, "evidence": ev, "score": ev[best]}


def _project(z, kind):
    z = np.asarray(z, float)
    if kind == "S6":
        nrm = np.linalg.norm(z, axis=1, keepdims=True)
        return z / np.maximum(nrm, 1e-12)
    if kind == "T6":
        return (z + np.pi) % (2 * np.pi) - np.pi
    return z


def _nll(z, y, kind, med):
    geo = _geodesic(_project(z, kind), kind)
    return -_gp_loglik(y, _rbf(geo, med))


def map_evidence(pts, seed=0, n_sub=80, n_steps=20, step=0.08):
    """MAP latents on each candidate, then GP evidence (docs/22).

    Stochastic ascent on the manifold (projected noise). Not Jensen ELBO,
    not H1, still does not recover T6.
    """
    rng = np.random.default_rng(seed)
    pts = rescale_to_unit(np.asarray(pts, float))
    if len(pts) > n_sub:
        pts = pts[rng.choice(len(pts), n_sub, replace=False)]
    w = rng.standard_normal(pts.shape[1])
    w /= np.linalg.norm(w)
    y = pts @ w
    y = y - y.mean()
    d = _pairwise(pts)
    inits = {
        "S6": (_sphere_latents(_mds(d, 7)), "S6"),
        "T6": (_torus_latents(_mds(d, 12)), "T6"),
        "R6": (_mds(d, 6), "R6"),
    }
    out = {}
    for name, (z, kind) in inits.items():
        geo0 = _geodesic(z, kind)
        med = float(np.median(geo0[np.triu_indices_from(geo0, k=1)]))
        med = max(med, 1e-3)
        best = -_nll(z, y, kind, med)
        for _ in range(n_steps):
            cand = _project(z + step * rng.standard_normal(z.shape), kind)
            sc = -_nll(cand, y, kind, med)
            if sc > best:
                best, z = sc, cand
        out[name] = float(best)
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def select_map_evidence(pts, seed=0, n_sub=80, n_steps=20, step=0.08):
    """MAP ranking only. Not an H1 verdict."""
    ev = map_evidence(pts, seed=seed, n_sub=n_sub, n_steps=n_steps, step=step)
    best = next(iter(ev))
    return {"geometry": best, "evidence": ev, "score": ev[best]}
