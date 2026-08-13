import numpy as np
from tpl.nulls.kuramoto import simulate_kuramoto
from tpl.analysis.triplet_phase import closure_naive, closure_windowed

def test_naive_closure_is_tautology():
    th = simulate_kuramoto(seed=2)
    assert closure_naive(np.sin(th[:, :3])) < 1e-8

def test_null_satisfies_windowed_closure():
    th = simulate_kuramoto(K=3.0, seed=2)
    assert closure_windowed(np.sin(th[:, :3])) < 0.5  # null passes the 'signature'
