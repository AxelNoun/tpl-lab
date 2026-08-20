# Chantier 12 — Calibration / analyse de puissance (amélioration 6)

Règle : AUCUNE analyse réelle avant d'avoir chiffré, sur synthétique, la capacité du
pipeline à distinguer S^d de T^d en fonction de (d, n, bruit).

Premier résultat (n = 1500, seed 0) — `python -m tpl.analysis.calibration` :
| d | topo TPR | topo FPR | ranking acc |
|---|---|---|---|
| 2 | 1,00 | 0,00 | 1,00 |
| 3 | 0,00 | 0,00 | 1,00 |

Lecture : la détection topologique directe (b1) meurt dès d = 3 à ce n — mais sans
faux positifs (critère conservateur). Le ranking par fingerprint garde une précision
parfaite. Conséquence protocolaire, gravée dans PREREGISTRATION.md : sur données
réelles, les mesures primaires sont le RANKING et le CONTRASTE ; b1 n'est qu'une
confirmation en basse dimension effective.

Grille complète (d = 2,3,4,6 ; n = 3000) : `python -m tpl.analysis.calibration --full`.

## Verdict H-TPL (conjonctif nommé) — `calibration --h1-power`

Compatible = ID dans une fenêtre prédite **et** géométrie = S⁶ par son nom.
n = 2000, 8 graines, `select_geometry n_boot=2` :

| données | attendu | TPR/TNR | ID dans fenêtre | géométrie S6 |
|---|---|---|---|---|
| S⁶ bruit 0,03 | compatible | 100 % | 100 % | 100 % |
| T⁶ (rival) | réfutée | 100 % | 25 % | 0 % (toujours T6) |
| R⁶ (rival) | réfutée | 100 % | **100 %** | 0 % |
| Kuramoto K=2 | réfutée | 100 % | 88 % | 0 % (aucun candidat) |
| gaussienne 20-D | réfutée | 100 % | 0 % | 0 % |

Lecture : la mesure 1 seule accepterait R⁶ à chaque fois et Kuramoto 7 fois sur 8
(fenêtre d = 8). C'est le *nom* S⁶ qui sépare. TwoNN sur le tore plat embarqué
lit souvent ~6,6 (dans le trou [6,5 ; 7,5[), donc T⁶ est déjà souvent rejeté par
la dimension ; R⁶ ne l'est pas.

## TPR(n) — `calibration --h1-power`

Règle **sans** le plancher n_min (8 graines). Le plancher n = 2000 du prereg ne
bouge pas : il vient de 200 graines sur TwoNN seul (14 % de réfutations à tort
à n = 1000). Huit graines ne suffisent pas à voir un taux de 14 %.

| n | TPR H-TPL (vrai S⁶) | ID dans fenêtre | S⁶ accepté | TNR rivaux / nuls |
|---|---|---|---|---|
| 500 | 88 % | 88 % | 100 % | 100 % |
| 1000 | 100 % | 100 % | 100 % | 100 % |
| 1500 | 100 % | 100 % | 100 % | 100 % |
| 2000 | 100 % | 100 % | 100 % | 100 % |

À n = 500, les 12 % de ratés sont **entièrement** la mesure 1 (TwoNN trop bas).
Le ranking S⁶ est déjà parfait. Le plancher n_min reste donc un plancher de
dimension, pas de géométrie.

## Bruit additif — `calibration --h1-noise`

Vrai S⁶, n = 2000, 8 graines :

| bruit σ | TPR H-TPL | ID ok | S⁶ accepté | aucun candidat |
|---|---|---|---|---|
| 0,03 | 100 % | 100 % | 100 % | 0 % |
| 0,08 | 88 % | 88 % | 100 % | 0 % |
| 0,12 | 50 % | 50 % | 100 % | 0 % |
| 0,15 | 12 % | 25 % | 12 % | 88 % |
| 0,20 | 0 % | 0 % | 0 % | 100 % |

Entre 0,08 et 0,12, TwoNN sort de la fenêtre **avant** que `MAX_FIT_SCORE` ne
rejette. À 0,15 le seuil d'adéquation fait ce pour quoi il a été calibré
(docs/09). Conséquence pour le réel : un rejet à score > 3,0 peut être du bruit
de mesure, pas une réfutation géométrique — déjà déclaré ; un rejet par ID trop
basse peut être la même chose à un bruit plus faible.
