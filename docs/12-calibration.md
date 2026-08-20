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
