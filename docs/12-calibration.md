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
À faire avant le prereg final : courbes TPR(n) par dimension pour chiffrer le n requis.
