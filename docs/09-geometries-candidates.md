# Chantier 9 — Inférence forte : quelle est la géométrie ? (améliorations 1, 2, 4)

Question reformulée (Platt 1964, *strong inference*) : « quelle est la géométrie des
états perceptifs soutenus ? ». S⁶ (TPL) n'est qu'un candidat parmi : T⁶ (tores —
prédiction naturelle des oscillateurs couplés, cf. Gardner et al. 2022 sur les grid
cells), R⁶ plat, et à terme un candidat hyperbolique. Un « négatif » devient une
découverte (« c'est un tore »).

## Arbre de décision
1. `rank_candidates(data)` — fingerprint (ID + distribution des distances par paires
   [Osada] + persistances H1), score Wasserstein, bootstrap. Validé : précision 1,0
   sur synthétique en dim 6 (voir demo).
2. `betti1(data)` — critère de gap sur H1. Discriminant net : S a b1=0, T^d a b1=d.
   ATTENTION : puissance nulle pour d ≥ 3 à n ≤ 3000 (voir calibration) ; en régime
   réel, b1 sert de confirmation basse dimension, pas de test principal.
3. Multiplets spectraux (docs/10) — structure fine, spécifique à S⁶/G2.

## Limites connues et upgrades prévus
- Le ranking est un CLASSEMENT, pas une probabilité postérieure. Étape suivante propre :
  modèles à variables latentes sur variétés avec vraisemblance marginale (mGPLVM,
  Jensen et al. 2020, *Manifold GPLVMs for discovering non-Euclidean latent structure
  in neural data*).
- Détection topologique en dim 6 : envisager cohomologie persistante / coordonnées
  circulaires, ou n >> 10⁴ (chiffrer via calibration --full).
- Sous-détermination : même un S⁶ confirmé ne prouverait pas les octonions — d'autres
  mécanismes engendrent des sphères. Le vocabulaire reste « compatible avec ».
