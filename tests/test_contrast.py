import pytest
from tpl.generative.manifolds import sphere, euclidean
from tpl.analysis.state_contrast import contrast

def test_contrast_detects_id_change():
    a = sphere(1500, dim=6, noise=0.02, seed=4)     # 'wake': structured, d=6
    b = euclidean(1500, dim=3, noise=0.02, seed=4)  # 'anesthesia': collapsed d=3
    c = contrast(a, b, n_boot=300, seed=4)
    assert c["delta_id"] > 1.5
    assert c["A"]["best_geometry"] == "S6"

def test_ci_is_stable_across_resampling_seeds():
    """Regression, audit v2: at the shipped n_boot=5 the 'CI95' was just the min
    and max of five draws and moved by more than a unit between seeds."""
    a = sphere(800, dim=6, noise=0.02, seed=4)
    b = euclidean(800, dim=3, noise=0.02, seed=4)
    los, his = [], []
    for s in (1, 2, 3):
        lo, hi = contrast(a, b, n_boot=300, seed=s)["delta_id_ci95"]
        assert hi > lo
        los.append(lo)
        his.append(hi)
    assert max(los) - min(los) < 0.4
    assert max(his) - min(his) < 0.4

def test_small_n_boot_warns():
    a = sphere(400, dim=6, noise=0.02, seed=4)
    b = euclidean(400, dim=3, noise=0.02, seed=4)
    with pytest.warns(RuntimeWarning, match="n_boot"):
        contrast(a, b, n_boot=5, seed=4)

def test_ci_stays_wider_than_the_rescaled_version():
    """Regression, audit v2: the sqrt(m/n) rescaling of Politis & Romano is the
    textbook fix for an interval computed at m < n, and measurement rejected it —
    coverage of the true difference fell from 98% to 65%. TwoNN's bias is
    invisible to subsampling, so the surplus width is the only thing
    compensating for it. Nobody may 'tidy' it away without re-running
    `calibration --ci-coverage`."""
    a = sphere(800, dim=6, noise=0.02, seed=4)
    b = euclidean(800, dim=3, noise=0.02, seed=4)
    c = contrast(a, b, n_boot=300, frac=0.632, seed=4)
    lo, hi = c["delta_id_ci95"]
    assert hi - lo > 0.5, "an interval this narrow means the rescaling crept back in"

def test_true_difference_is_underestimated_not_overestimated():
    """The direction that keeps 'CI95 excludes 0' conservative: TwoNN's bias grows
    with d, so a positive difference comes out too SMALL, never too large."""
    a = sphere(1500, dim=6, noise=0.02, seed=11)
    b = sphere(1500, dim=3, noise=0.02, seed=11)
    c = contrast(a, b, n_boot=300, seed=11)
    assert c["delta_id"] < 3.0, "true difference is 3; overestimating it would be unsafe"
    assert c["delta_id"] > 2.0
