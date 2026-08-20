# Chantier 9 — Inférence forte : quelle est la géométrie ? (améliorations 1, 2, 4)

Question reformulée (Platt 1964, *strong inference*) : « quelle est la géométrie des
états perceptifs soutenus ? ». S⁶ (TPL) n'est qu'un candidat parmi : T⁶ (tores —
prédiction naturelle des oscillateurs couplés, cf. Gardner et al. 2022 sur les grid
cells), R⁶ plat, et à terme un candidat hyperbolique. Un « négatif » devient une
découverte (« c'est un tore »).

## Arbre de décision
1. `select_geometry(data)` — classe les candidats PUIS vérifie que le gagnant
   convient vraiment. Le fingerprint (ID + distribution des distances par paires
   [Osada] + persistances H1, score Wasserstein) est invariant d'échelle depuis
   l'audit v2. Utiliser `rank_candidates` seul est insuffisant : il désigne
   toujours un gagnant, donc « S⁶ a gagné » vaut 1 chance sur 3 par défaut.
2. `betti1(data)` — critère de gap sur H1. Discriminant net : S a b1=0, T^d a b1=d.
   ATTENTION : puissance nulle pour d ≥ 3 à n ≤ 3000 (voir calibration) ; en régime
   réel, b1 sert de confirmation basse dimension, pas de test principal.
3. Multiplets spectraux (docs/10) — structure fine, spécifique à S⁶/G2.

## Seuil d'adéquation absolu (audit v2, figé avant données réelles)

`MAX_FIT_SCORE = 3,0`. Reproduire : `python -m tpl.analysis.calibration --fit-threshold`.
Calibré à n = 2000, 4 graines par cellule, sur du synthétique uniquement (règle 2).

| Classe | Score min–max |
|---|---|
| S⁶ bruit 0,03 / 0,10 | 0,26–0,55 / 1,42–1,91 |
| S⁶ NON uniforme (densité repondérée) | 2,07–2,56 |
| T⁶ / R⁶ bruit 0,03 | 0,43–0,62 / 0,69–1,03 |
| S³ / S¹⁰ / T³ | 11,01–12,02 / 4,05–4,32 / 6,21–7,25 |
| Gaussienne 20-D | 13,30–14,60 |
| Nul de Kuramoto K=0 / K=2 | 4,20–19,82 / 29,05–58,05 |

Marge de séparation [2,56 ; 4,05] ; 3,0 est au milieu et penche vers le rejet, comme
le critère de gap de `betti1`. Sur cette grille : 0 % de faux positifs, 0 % de faux
négatifs. Le nul du projet est rejeté (règle 1 satisfaite) : le classement S⁶ n'est
pas quelque chose qu'un Kuramoto obtient gratuitement.

LIMITE DÉCLARÉE : un VRAI S⁶ portant un bruit ≥ 0,15 dépasse aussi 3,0 (3,34 à 0,15 ;
4,63 à 0,20) et se fait rejeter. Au-delà de ce niveau de bruit le test n'a plus de
puissance — il ne se trompe pas, il ne conclut plus. À chiffrer sur les données réelles
avant de conclure quoi que ce soit d'un rejet. Le score est en revanche stable en n
(0,52–0,66 de n = 500 à n = 3000).

## Limites connues et upgrades prévus
- Le ranking est un CLASSEMENT, pas une probabilité postérieure. Étape suivante propre :
  modèles à variables latentes sur variétés avec vraisemblance marginale (mGPLVM,
  Jensen et al. 2020, *Manifold GPLVMs for discovering non-Euclidean latent structure
  in neural data*).
- Détection topologique en dim 6 : envisager cohomologie persistante / coordonnées
  circulaires, ou n >> 10⁴ (chiffrer via calibration --full).
- Sous-détermination : même un S⁶ confirmé ne prouverait pas les octonions — d'autres
  mécanismes engendrent des sphères. Le vocabulaire reste « compatible avec ».
