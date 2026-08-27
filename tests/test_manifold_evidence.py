"""Geodesic-GP evidence (mGPLVM stand-in) and degenerate-contrast gate."""

import numpy as np
import pytest

from tpl.analysis.manifold_evidence import (
    evidence,
    map_evidence,
    select_evidence,
    select_map_evidence,
)
from tpl.analysis.state_contrast import contrast, unique_fraction
from tpl.generative.manifolds import euclidean, sphere, torus_flat
from tpl.nulls.kuramoto import simulate_kuramoto


def test_sphere_evidence_prefers_s6():
    ev = evidence(sphere(600, dim=6, noise=0.02, seed=1), seed=1, n_sub=250)
    assert next(iter(ev)) == "S6"


def test_torus_evidence_does_not_name_s6():
    """Isotropic geodesic T6 does not recover the product embedding (docs/22)."""
    ev = evidence(torus_flat(600, dim=6, noise=0.02, seed=2), seed=2, n_sub=250)
    assert next(iter(ev)) != "S6"


def test_kuramoto_is_not_named_s6_by_evidence():
    th = simulate_kuramoto(n=12, n_steps=4000, seed=0)
    pts = np.sin(th)
    assert select_evidence(pts, seed=0, n_sub=250)["geometry"] != "S6"


def test_euclidean_evidence_does_not_name_s6():
    ev = evidence(euclidean(600, dim=6, noise=0.02, seed=0), seed=0, n_sub=250)
    assert next(iter(ev)) != "S6"
    sel = select_evidence(euclidean(500, dim=6, noise=0.02, seed=0), seed=0, n_sub=200)
    assert "geometry" in sel and "evidence" in sel


def test_duplicate_cloud_skips_ci_without_changing_n_boot():
    a = sphere(400, dim=6, noise=0.02, seed=4)
    b = np.zeros((400, 7))
    assert unique_fraction(b) < 0.2
    with pytest.warns(RuntimeWarning, match="CI skipped"):
        c = contrast(a, b, n_boot=300, seed=4)
    assert c["delta_id_ci95"] is None
    assert c["n_boot"] == 300
    assert c["ci_reason"] == "degenerate_duplicates"


def test_map_evidence_is_a_ranking_not_h1():
    """Stochastic MAP is more flexible than frozen MDS: a sphere may name R6.
    That is not a reason to feed it to h1_verdict (docs/22)."""
    ev = map_evidence(
        sphere(400, dim=6, noise=0.02, seed=1), seed=1, n_sub=80, n_steps=12
    )
    assert set(ev) == {"S6", "T6", "R6"}
    sel = select_map_evidence(
        euclidean(300, dim=6, noise=0.02, seed=0), seed=0, n_sub=80, n_steps=8
    )
    assert "geometry" in sel and "evidence" in sel
    assert sel["geometry"] != "S6"
