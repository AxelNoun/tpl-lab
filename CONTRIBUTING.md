# Contributing

Read `CLAUDE.md` first. This lab **falsifies** a conjecture; it does not defend it.

- Do not retune thresholds, windows, filters, `n_min`, `MAX_FIT_SCORE`, or
  `h1_geometry` after `prereg-v1`. That tag is the analysis plan.
- Every confirmatory signature must beat a null in `src/tpl/nulls/`.
- Simulated artefacts: prefix `synth_`. Never commit raw `data/` (except
  `data/README.md`).
- Code and docstrings in English; `docs/` in French.
- `pytest -q` before concluding. `ruff format` before a commit if you have ruff.
- Vocabulary: “compatible with” ≠ “demonstrates”. Do not write “proves that”.

Useful entry points that are *not* “run another Allen session until S⁶ appears”:
geodesic-GP / MAP evidence (docs/22, secondary). IBL at 50 ms is INDECIDABLE
(docs/18–19). Claar: docs/21 and docs/23 (do not shop a third mouse).
OSF deposit: docs/24. Lab ask: docs/26. Manuscript: paper/registered-report.md.
The structured low-rank RNN is in docs/20.
