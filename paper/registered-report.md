# Pre-registered falsification of an S⁶ geometry of cortical population dynamics

TPL-Lab. Stage-2-style report of git tag `prereg-v1`
(`0a5e794477c788f174f623465177b0ffee08c880`, 20 August 2026).

This document cannot be submitted as a Stage 1 Registered Report: data were
analysed after the freeze. It *is* the report of that freeze. Vocabulary:
“compatible with” is not “demonstrates”. A clean negative is the intended
product.

## Abstract

A public Substack conjecture (VSA-TOE / topological phase-locking) claimed
that cortical dynamics during a sustained percept live on S⁶ ≅ G₂/SU(3).
We cut that claim down to what a passive spike recording can test: the
cloud of 50 ms population count vectors in one cortical area should have
TwoNN dimension in [5.5, 6.5) or [7.5, 8.5) **and** be accepted as S⁶ by
a named geometry test (`select_geometry`, cutoff 3.0), not T⁶, not R⁶, not
“no candidate”. The rule, windows, and cutoffs were frozen in
`PREREGISTRATION.md` / `configs/prereg_v1.json` before any real extract.
On Allen Visual Coding Neuropixels, H1-spontaneous is refuted in 12/12
visual-area tests (two mice). An IBL VISp insertion is INDECIDABLE
(decorrelation leaves n < 2000). On DANDI 000458 (Claar et al.), wake and
isoflurane both refute H1 in two animals (prelimbic then secondary motor).
A drop in TwoNN ID under isoflurane, when it occurs, does not restore S⁶.
We do not retune thresholds after seeing data.

## Introduction

The source essay is a starting point to test, not a scientific reference.
What remains testable on passive data is a **named** 6-sphere in the
ambient space of spike counts R^N, N ≥ 7, one area, no PCA to 7 (docs/01,
docs/02). Phase-triplet closure is algebraically tautological (docs/03).
Octonionic non-associativity is not a prediction from a passive trace
(docs/05). Spectral G₂ multiplets are statements about S⁶ ⊂ R⁷ and do not
apply to mixed N-channel recordings (docs/10).

Strong inference: among {S⁶, T⁶, R⁶, none}, H-TPL is S⁶. A fitted T⁶ or
R⁶ is a rival, not a soft confirmation.

## Methods (frozen)

Full rule: `PREREGISTRATION.md` at `prereg-v1`. Pipeline:

```
python -m tpl.analysis.run_id --config configs/prereg_v1.json --data X.npy --seed 42
```

- Observable: non-overlapping 50 ms spike counts, one CCF area, quality
  filters of the dataset authors only.
- No z-score, no rate cut, no reduction to R⁷.
- Decimate until mean autocorrelation < 0.1 (`decorrelate`). Cap →
  INDECIDABLE (series never independent).
- n ≥ 2000 after decimation or INDECIDABLE (TwoNN false-refutation of a
  true S⁶ is 14 % at n = 1000, 1 % at n = 2000).
- Measure 1: TwoNN ID in half-open windows around 6 or 8, ±0.5.
- Measure 2: `select_geometry` must name S⁶ with score ≤ 3.0.
- H1 is conjunctive. Rank-only winning is not enough (`rank_candidates`
  always names someone).
- Contrast (when two states exist): delta ID (wake − anesthesia) > 0 with
  a 1000-draw without-replacement subsample CI, **and** geometry ≠ S⁶
  under anesthesia. The CI is a detection test, not an effect size
  (`calibration --ci-coverage`).
- Concatenating short trials is forbidden.

Nulls already beaten on synthetic geometry: Kuramoto, phase-randomized
surrogates (`preserve_cross=True`), chaotic RNN, structured rank-6 RNN
(docs/20). A test the null also passes is logged as non-discriminant.

Secondary geodesic-GP / MAP latents (docs/22) never enter `h1_verdict`.

## Results

### Allen H1-spontaneous — 12/12 refuted

Longest single `spontaneous` block, awake, `quality==good`, seed 42.

Session `767871931` (docs/14–15), 1802.5 s block:

| Area | n | ID | geometry (score) | H1 |
|---|---|---|---|---|
| VISp | 7210 | 37.07 | none (R6 41.68) | refuted |
| VISal | 6009 | 26.87 | none (T6 29.92) | refuted |
| VISam | 5150 | 24.42 | none (T6 28.01) | refuted |
| VISpm | 36050 | 32.77 | none (T6 35.35) | refuted |
| VISrl | 6009 | 26.54 | none (T6 29.61) | refuted |
| VISli | 7210 | 26.82 | none (T6 28.70) | refuted |
| phase-null VISp | 7210 | 42.85 | none (R6 63.32) | refuted |

Session `766640955`, other mouse, declared before the NWB (docs/16): 6/6
refuted. Two areas ranked S⁶ first at score ~25–27; `select_geometry`
refused. Rank-only would have lied.

### IBL — INDECIDABLE

VISp insertion `a8a59fc3-…` (docs/17–19), rule written before spikes.
Spontaneous 600 s → n = 1334 after lag 9. Full clock ~97 min →
autocorrelation never < 0.1 in 1000 lags → n = 118. Both INDECIDABLE.
The 0.1 rule is not loosened.

### Claar wake / isoflurane — H1 refuted both animals

DANDI 000458. Smallest NWB with `Units`, then the next-smallest other
subject. Modal area, not a hunt for S⁶.

`sub-551399` PL (docs/21): wake ID 39.20, none (T6 43.89); isoflurane
ID 29.64, none (S6 score nan; ~92 % duplicate 50 ms bins). H1 refuted
both. CI at n_boot = 1000 not published on that degenerate cloud.

`sub-590479` MOs (docs/23): wake ID 25.98, none (R6 28.92); isoflurane
ID 21.35, none (R6 68.59). H1 refuted both. Contrast n_boot = 1000:
delta ID 4.64, CI95 [3.93, 5.68] excludes 0 (detection, not an effect
size). ID falls; S⁶ does not appear. TPL is not restored.

### Synthetic adversaries

Structured overlap rank-6 RNN (docs/20): n = 8236, ID = 14.95, none
(R6 36.76), H1 refuted. Rank 6 in W is not S⁶. Geodesic-GP names S⁶ on
true spherical samples and does not name it on T⁶, R⁶, or Kuramoto; it
does not recover T⁶ (docs/22).

## Discussion

What this shows: the amputated, pre-registered claim is incompatible with
these public Neuropixels recordings under the frozen rule.

What this does not show: that cortex has no manifold; that a 10 s
controlled percept was tested (underpowered; concatenation forbidden);
that octonions were tested; that PCI was tested (Claar is cortical
electrical stimulation, not TMS-EEG).

Remaining work that is not fishing: click *Register* on
https://osf.io/fgvpz/ for a DOI if wanted (irreversible; docs/24);
causal non-associativity and structural psychophysics need a lab
(docs/05, docs/08); a variational mGPLVM remains secondary.

## Data and code

MIT. https://github.com/AxelNoun/tpl-lab  
Tag `prereg-v1` = `0a5e794`. Replay:
`python -m tpl.analysis.run_id --config configs/prereg_v1.json --synthetic`

Allen: Siegle et al., *Nature* (2021). IBL Brain-wide Map. Claar et al.,
DANDI 000458. Raw NWBs are not in git.
