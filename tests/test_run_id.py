"""Regression tests for the preregistered pipeline (audit v2, F4/F5/F7)."""

import json
from pathlib import Path

import numpy as np
import pytest

from tpl.analysis.intrinsic_dim import autocorrelation_time, decorrelate, twonn
from tpl.analysis.model_comparison import MAX_FIT_SCORE
from tpl.analysis.run_id import classify_id, h1_verdict, load_config, run_condition
from tpl.generative.s6_flow import sample_s6_uniform, simulate_s6
from tpl.generative.manifolds import euclidean

CONFIG = Path(__file__).resolve().parents[1] / "configs" / "prereg_v1.json"
TARGETS, TOL = [6, 8], 0.5


def test_config_matches_the_calibrated_constant():
    """The config must not quietly drift away from the code it parameterises."""
    cfg = load_config(CONFIG)
    assert cfg["geometry"]["max_fit_score"] == MAX_FIT_SCORE
    assert cfg["geometry"]["h1_geometry"] == "S6"
    assert cfg["intrinsic_dimension"]["targets"] == TARGETS
    assert cfg["intrinsic_dimension"]["min_samples_after_decimation"] == 2000


def test_load_config_rejects_a_retuned_threshold():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    cfg["geometry"]["max_fit_score"] = 99.0
    tmp = CONFIG.parent / "_tmp_retuned.json"
    tmp.write_text(json.dumps(cfg), encoding="utf-8")
    try:
        with pytest.raises(ValueError, match="HARKing"):
            load_config(tmp)
    finally:
        tmp.unlink()


def test_load_config_rejects_a_lowered_n_min():
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    cfg["intrinsic_dimension"]["min_samples_after_decimation"] = 500
    tmp = CONFIG.parent / "_tmp_nmin.json"
    tmp.write_text(json.dumps(cfg), encoding="utf-8")
    try:
        with pytest.raises(ValueError, match="frozen"):
            load_config(tmp)
    finally:
        tmp.unlink()


@pytest.mark.parametrize(
    "value,expected",
    [
        (4.0, "refutee"),  # below every prediction
        (5.49, "refutee"),
        (5.5, "compatible"),  # window for d = 6 opens
        (6.0, "compatible"),
        (6.49, "compatible"),
        (6.5, "refutee"),  # between the two predicted integers
        (7.0, "refutee"),
        (7.49, "refutee"),
        (7.5, "compatible"),  # window for d = 8 opens
        (8.49, "compatible"),
        (8.5, "refutee"),  # above every prediction
        (11.0, "refutee"),
    ],
)
def test_decision_rule_at_every_boundary(value, expected):
    assert classify_id(value, TARGETS, TOL)[0] == expected


def test_decision_rule_is_exhaustive():
    """F7: the prose version left ID < 5.5 unclassified. Every real value must
    now land in exactly one verdict."""
    for value in np.arange(0.0, 15.0, 0.01):
        assert classify_id(float(value), TARGETS, TOL)[0] in ("compatible", "refutee")


def test_decision_rule_is_never_looser_than_the_original_wording():
    """The original text refuted [6.5, 7.5] and > 8.5; those must still refute."""
    for value in (6.5, 7.0, 7.49, 8.6, 9.0):
        assert classify_id(value, TARGETS, TOL)[0] == "refutee"


def test_iid_data_needs_no_decimation():
    assert autocorrelation_time(sample_s6_uniform(2000, seed=1)) == 1


def test_smooth_trajectory_is_thinned():
    traj = simulate_s6(n_steps=4000, seed=1)
    thinned, lag = decorrelate(traj)
    assert lag > 1
    assert len(thinned) == len(traj[::lag])


def test_decimation_removes_the_downward_bias():
    """F5: the whole point of the rule. Undecimated autocorrelated data reads
    well below the true d = 6; the data-derived factor recovers it."""
    traj = simulate_s6(n_steps=20000, seed=1)
    thinned, _ = decorrelate(traj)
    assert twonn(traj) < 5.0
    assert 5.5 <= twonn(thinned) < 6.5


def test_short_recording_is_declared_undecidable_not_refuted():
    """F6: TwoNN converges to d from BELOW, so a short recording refutes a
    CORRECT hypothesis 14% of the time at n = 1000. Withholding the verdict is
    the only honest output."""
    res = run_condition(sample_s6_uniform(300, seed=2), load_config(CONFIG))
    assert res["verdict"] == "indecidable"
    assert "id" not in res, "no estimate may be reported below the power floor"


def test_too_few_channels_is_refused_not_padded():
    """Bridge law: S^6 cannot sit in R^6. Padding or PCA-up is forbidden."""
    with pytest.raises(ValueError, match="cannot sit"):
        run_condition(np.ones((500, 6)), load_config(CONFIG))


def test_h1_requires_s6_by_name_not_any_fitted_candidate():
    assert h1_verdict("compatible", "S6") == "compatible"
    assert h1_verdict("compatible", "T6") == "refutee"
    assert h1_verdict("compatible", "R6") == "refutee"
    assert h1_verdict("compatible", None) == "refutee"
    assert h1_verdict("refutee", "S6") == "refutee"


def test_a_fitted_euclidean_6d_refutes_tpl():
    """R^6 has ID in the d = 6 window and clears MAX_FIT_SCORE, so the old
    conjunctive rule (any accepted candidate) would have called it compatible.
    It is a rival, not TPL."""
    pts = euclidean(2000, dim=6, noise=0.03, seed=1)
    from tpl.analysis.model_comparison import select_geometry

    d = twonn(pts)
    id_v, _ = classify_id(d, TARGETS, TOL)
    sel = select_geometry(pts, seed=1, n_boot=2)
    assert id_v == "compatible", f"ID = {d:.2f} should sit in the d = 6 window"
    assert sel["geometry"] == "R6"
    assert h1_verdict(id_v, sel["geometry"]) == "refutee"


def test_true_s6_is_compatible_on_both_measures():
    pts = sample_s6_uniform(2000, seed=3)
    from tpl.analysis.model_comparison import select_geometry

    d = twonn(pts)
    id_v, _ = classify_id(d, TARGETS, TOL)
    sel = select_geometry(pts, seed=3, n_boot=2)
    assert id_v == "compatible"
    assert sel["geometry"] == "S6"
    assert h1_verdict(id_v, sel["geometry"]) == "compatible"


def test_geodesic_gp_is_printed_after_h1_and_cannot_change_it():
    """docs/22: secondary ranking is stored on the result, never passed to
    h1_verdict. A true S6 stays compatible even if the GP names something else."""
    pts = sample_s6_uniform(2000, seed=3)
    res = run_condition(pts, load_config(CONFIG))
    assert res["verdict"] == "compatible"
    assert "evidence_geometry" in res
    assert "evidence" in res
    # The frozen conjunctive rule still only sees select_geometry.
    assert h1_verdict(res["id_verdict"], res["geometry"]) == res["verdict"]
