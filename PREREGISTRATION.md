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

## Mesures primaires (révision v3, post-audit v2)
1. PRIMAIRE : `select_geometry` — S⁶ doit gagner contre T⁶/R⁶ en veille ET passer le
   seuil d'adéquation absolu `MAX_FIT_SCORE = 3,0` (figé, calibré sur synthétique,
   docs/09). Gagner ne suffit pas : `rank_candidates` seul désigne toujours un
   vainqueur, donc « S⁶ a gagné » vaudrait 1 chance sur 3 par défaut. Un score > 3,0
   se lit « aucune des trois géométries », pas « S⁶ affaibli ».
2. PRIMAIRE : `contrast` veille vs anesthésie — delta ID > 0 avec CI95 excluant 0
   (intervalle par SOUS-ÉCHANTILLONNAGE SANS REMISE, n_boot ≥ 1000 : le bootstrap avec
   remise est invalide pour un estimateur k-NN, audit v2), ET perte de l'acceptation
   de S⁶ sous anesthésie (`best_geometry` ≠ "S6", y compris None).
3. SECONDAIRE : b1 (gap) = 0 attendu ; interprétable seulement si dim effective ≤ 3.
4. EXPLORATOIRE (risqué, déclaré tel) : multiplets spectraux 7/27 (docs/10).

## Analyse (figée)
Pipeline exact : `python -m tpl.analysis.run_id --config configs/prereg_v1.yaml`.
Seed 42. Aucun paramètre libre après le tag.
