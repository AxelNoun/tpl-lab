"""Upgrade #5b — derived spectral predictions, CORRECTED after audit v1.

AUDIT FINDING: the earlier claim of 'plateaus of 7 then 27' was WRONG as
stated. In the raw feature basis {x_i, x_i x_j}, the G2-irreducible 27-dim
harmonic space H2 appears SPLIT into 6 + 21 blocks, because that basis is not
orthonormal in L2(S^6). The representation is irreducible; the basis was not.

Corrected prediction A (exact, sphere-specific): for uniform S^6 data, the
covariance spectrum of degree-<=2 raw features has EXACTLY four levels:
  1/7  (x7)   [H1 harmonics]
  2/63 (x6)   [traceless diagonal part of H2]
  1/63 (x21)  [off-diagonal part of H2]
  0    (x1)   [the trace direction: x.x = 1]
Verified numerically to 4 decimals at n = 60000. A Gaussian/torus cloud does
not match this rational profile.

Corrected prediction B (Schur): in an ORTHONORMAL harmonic basis, any
O(7)-invariant measure has block-scalar covariance: c1*I on H1 (7) and
c2*I on H2 (27) — the true '7/27 multiplet' statement. Anisotropic
deformations (and realistic linear mixing!) break it; alignment/whitening
before testing is a documented prerequisite (see docs/10, docs/02).
"""
import numpy as np

# Single source of truth for the four exact levels: matches_s6_profile reads its
# targets from here rather than restating them (audit v2, F11).
THEORY_S6 = np.array([1/7]*7 + [2/63]*6 + [1/63]*21 + [0.0])


def quad_features(pts):
    x = np.asarray(pts, float)
    iu = np.triu_indices(x.shape[1])
    quad = (x[:, :, None] * x[:, None, :])[:, iu[0], iu[1]]
    return np.concatenate([x, quad], axis=1)


def covariance_spectrum(pts):
    f = quad_features(pts)
    f = f - f.mean(0)
    return np.linalg.eigvalsh(np.cov(f.T))[::-1]


def matches_s6_profile(evals, rtol=0.15):
    """Do the sorted eigenvalues match the exact 4-level S^6 theory?

    PRECONDITION: the data must lie on the UNIT sphere. 1/7, 2/63 and 1/63 are
    absolute values, not ratios, so a uniform rescaling by 2 fails the test on
    data that is still a perfect S^6 (audit v2, F10). Rotations are harmless.
    Noise costs power quickly: passes at sigma = 0.05, fails at 0.10.
    Rescale before calling; the check below only catches the gross case, since
    a radius that merely drifts still breaks the absolute levels.
    """
    ev = np.asarray(evals)[:35]
    if ev.size < 35:
        return False
    blocks = [ev[:7], ev[7:13], ev[13:34]]
    targets = THEORY_S6[[0, 7, 13]]
    lvl = all(abs(b.mean() - t) < rtol * t and np.ptp(b) < 2 * rtol * t
              for b, t in zip(blocks, targets))
    return bool(lvl and ev[34] < 0.2 * THEORY_S6[13])


def harmonic_features_on(pts):
    """Orthonormal (w.r.t. uniform S^6 measure) basis of H1 (+) H2: 7 + 27.
    y_i = sqrt(7) x_i ; z_ij = sqrt(63) x_i x_j (i<j) ;
    w_a = sqrt(63/2) sum_i c_ai (x_i^2 - 1/7), {c_a} ON basis of (1,...,1)^perp."""
    x = np.asarray(pts, float)
    d = x.shape[1]
    y = np.sqrt(d) * x
    iu = np.triu_indices(d, k=1)
    z = np.sqrt(d * (d + 2)) * (x[:, :, None] * x[:, None, :])[:, iu[0], iu[1]]
    ones = np.ones((d, 1)) / np.sqrt(d)
    Q, _ = np.linalg.qr(np.eye(d) - ones @ ones.T)
    C = Q[:, :d-1]  # ON basis of the traceless diagonal directions
    w = np.sqrt(d * (d + 2) / 2.0) * (x**2 - 1.0/d) @ C
    return np.concatenate([y, w, z], axis=1)


def schur_block_scores(pts):
    """Off-scalar deviation of covariance per irrep block (H1, H2), ON basis.
    ~0 for O(7)-invariant measures; large under anisotropy/mixing."""
    f = harmonic_features_on(pts)
    f = f - f.mean(0)
    Cv = np.cov(f.T)
    d = pts.shape[1]
    n1 = d
    out = {}
    for name, sl in (("H1", slice(0, n1)), ("H2", slice(n1, Cv.shape[0]))):
        B = Cv[sl, sl]
        c = np.trace(B) / B.shape[0]
        out[name] = float(np.linalg.norm(B - c*np.eye(B.shape[0])) / (c*np.sqrt(B.shape[0])))
    return out
