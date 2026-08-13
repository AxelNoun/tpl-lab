from tpl.generative.manifolds import sphere, euclidean
from tpl.analysis.state_contrast import contrast

def test_contrast_detects_id_change():
    a = sphere(1500, dim=6, noise=0.02, seed=4)     # 'wake': structured, d=6
    b = euclidean(1500, dim=3, noise=0.02, seed=4)  # 'anesthesia': collapsed d=3
    c = contrast(a, b, n_boot=4, seed=4)
    assert c["delta_id"] > 1.5
    assert c["A"]["best_geometry"] == "S6"
