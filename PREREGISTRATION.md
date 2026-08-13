# Pré-enregistrement — chantier 6 (dimension intrinsèque)
**Statut : BROUILLON — à figer avant tout contact avec des données réelles.**
Une fois figé : tag git `prereg-v1`, dépôt du hash sur OSF, aucune modification.

## H1 (TPL) 
Pendant un stimulus perceptif constant (>10 s), la dimension intrinsèque (ID) de la
dynamique de population corticale, estimée par TwoNN sur les vecteurs de population
(fenêtres de 50 ms, NON chevauchantes, décimées jusqu'à autocorrélation < 0,1 — le biais d'autocorrélation sous-estime l'ID, voir tests/test_dim.py), sature à **d = 6** (variante : d = 8). Tolérance déclarée : ±0,5.

## H0
L'ID ne se distingue pas de celle produite par (a) un Kuramoto ajusté aux mêmes
spectres, (b) des surrogates à phase randomisée des mêmes données.

## Critères de réfutation (déclarés à l'avance)
- Si ID médiane ∈ [6,5 ; 7,5] ou > 8,5 de façon robuste : H1 réfutée.
- Si les nuls reproduisent l'ID observée à ±0,5 : test déclaré non-discriminant.
- Si l'ID ne change pas entre veille et anesthésie/sommeil profond (jeux de données
  avec états contrastés) : H1 fortement affaiblie.

## Données visées (ordre de priorité)
1. Allen Brain Observatory — Visual Coding Neuropixels (stimuli constants, veille).
2. IBL Brain-wide Map (Neuropixels, tâche standardisée).
3. EEG haute densité OpenNeuro avec conditions veille/anesthésie.

## Mesures primaires (révision v2, post-calibration)
1. PRIMAIRE : `rank_candidates` — S⁶ doit gagner contre T⁶/R⁶ en veille.
2. PRIMAIRE : `contrast` veille vs anesthésie — delta ID > 0, CI95 excluant 0,
   et perte du classement S⁶ sous anesthésie.
3. SECONDAIRE : b1 (gap) = 0 attendu ; interprétable seulement si dim effective ≤ 3.
4. EXPLORATOIRE (risqué, déclaré tel) : multiplets spectraux 7/27 (docs/10).

## Analyse (figée)
Pipeline exact : `python -m tpl.analysis.run_id --config configs/prereg_v1.yaml`.
Seed 42. Aucun paramètre libre après le tag.
