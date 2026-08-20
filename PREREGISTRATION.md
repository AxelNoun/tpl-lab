# Pré-enregistrement — chantier 6 (dimension intrinsèque)
**Statut : BROUILLON — à figer avant tout contact avec des données réelles.**
Une fois figé : tag git `prereg-v1`, dépôt du hash sur OSF, aucune modification.

## H1 (TPL) 
Pendant un stimulus perceptif constant (>10 s), la dimension intrinsèque (ID) de la
dynamique de population corticale, estimée par TwoNN sur les vecteurs de population
(fenêtres de 50 ms, NON chevauchantes, décimées jusqu'à autocorrélation < 0,1 —
le biais d'autocorrélation sous-estime l'ID, voir tests/test_dim.py), sature à
**d = 6** (variante : d = 8). Tolérance déclarée : ±0,5.

La décimation est calculée par `intrinsic_dim.decorrelate`, jamais fixée à la
main : sur une rotation S⁶ de vraie dimension 6, les facteurs 1 / 2 / 5 / 10
donnent 4,05 / 4,49 / 5,40 / 6,01 — le choix de l'analyste déciderait à lui seul
du verdict.

## H0
L'ID ne se distingue pas de celle produite par (a) un Kuramoto ajusté aux mêmes
spectres, (b) des surrogates à phase randomisée des mêmes données.

## Critères de réfutation (déclarés à l'avance, révisés audit v2)
La règle sur l'ID est **exhaustive et sans recouvrement** : tout réel tombe dans
exactement une case. Fenêtres d'acceptation semi-ouvertes `[t−0,5 ; t+0,5[`.
Implémentation et tests aux bornes : `run_id.classify_id`, `tests/test_run_id.py`.

| ID médiane | verdict |
|---|---|
| < 5,5 | **réfutée** — variété de dimension plus basse que prédit |
| [5,5 ; 6,5[ | compatible avec d = 6 |
| [6,5 ; 7,5[ | **réfutée** — entre les deux entiers prédits |
| [7,5 ; 8,5[ | compatible avec d = 8 (variante) |
| ≥ 8,5 | **réfutée** — variété de dimension plus haute que prédit |

La version antérieure laissait `ID < 5,5` non classée (un effondrement à d = 3
n'était donc *ni* compatible *ni* réfutant) et plaçait 6,5 et 7,5 simultanément
dans une case d'acceptation et une case de réfutation. La règle ci-dessus n'est
plus permissive que l'ancienne en aucun point.

**Puissance minimale — n ≥ 2000 échantillons APRÈS décimation.** TwoNN converge
vers d par le bas : sur un vrai S⁶, la règle ci-dessus réfute à tort dans
36,5 % des cas à n = 250 ; 17,5 % à n = 500 ; 14,0 % à n = 1000 ; 2,5 % à
n = 1500 ; 1,0 % à n = 2000 (200 graines par point). En dessous du plancher,
`run_id` renvoie **INDÉCIDABLE** et ne publie aucune estimation : conclure y
serait réfuter le bruit d'estimation. Conséquence expérimentale à assumer avant
d'enregistrer : avec un facteur de décimation typique de 25 à 55, il faut
50 000 à 110 000 fenêtres de 50 ms par condition, soit **45 min à 1 h 30 de
signal continu**.

- Si les nuls reproduisent l'ID observée à ±0,5 : test déclaré non-discriminant.
  **Ce cas est déjà avéré** : un Kuramoto de 12 oscillateurs décimé selon la même
  règle donne ID = 8,23, à l'intérieur de la fenêtre d'acceptation de la variante
  d = 8. La mesure 1 seule ne discrimine donc pas tant que la variante d = 8 est
  autorisée ; c'est la mesure 2 (géométrie) qui sépare (score 55,8 contre 0,47).
  Le verdict H1 est en conséquence **conjonctif** : dimension ET géométrie.
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
   **L'IC95 est un test de détection, pas une taille d'effet, et sera publié comme
   tel.** Couverture mesurée de la vraie différence : 98 % pour un contraste 6 contre 3,
   mais 40 % pour 10 contre 3, le biais de TwoNN dépassant alors la largeur de
   l'intervalle (docs/11, `calibration --ci-coverage`). Le biais croissant avec d, la
   différence est sous-estimée et l'intervalle tiré vers zéro : « exclut 0 » reste donc
   conservateur. Interdiction déclarée à l'avance : ne jamais rapporter la largeur de
   cet intervalle comme barre d'erreur, ni delta ID comme amplitude d'effondrement.
3. SECONDAIRE : b1 (gap) = 0 attendu ; interprétable seulement si dim effective ≤ 3.
4. EXPLORATOIRE (risqué, déclaré tel) : multiplets spectraux 7/27 (docs/10).

## Analyse (figée)
Pipeline exact, existant et exécutable :

```bash
python -m tpl.analysis.run_id --config configs/prereg_v1.json --data X.npy
python -m tpl.analysis.run_id --config configs/prereg_v1.json --synthetic  # dry-run
```

Seed 42. Aucun paramètre libre après le tag : tout ce qui pourrait devenir un
degré de liberté d'analyste (seuil d'autocorrélation, tolérance, n minimal,
bornes d'acceptation, `MAX_FIT_SCORE`, n_boot) est lu dans le fichier de config
et réaffiché dans la sortie. `load_config` refuse un `max_fit_score` modifié.
Format JSON et non YAML : pas de dépendance hors numpy/scipy dans le cœur
(CLAUDE.md). Le dry-run `--synthetic` sert à faire relire le pipeline **avant**
de figer le tag ; ses sorties sont préfixées `synth_` et n'ont aucune valeur
empirique.
