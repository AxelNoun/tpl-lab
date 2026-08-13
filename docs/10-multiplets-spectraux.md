# Chantier 10 — Prédictions spectrales G2 (RÉVISÉ après audit v1)

## Erreur trouvée et corrigée
La v1 annonçait « plateaux de multiplicités 7 puis 27 ». C'était FAUX tel qu'énoncé :
dans la base brute {x_i, x_i x_j}, l'espace harmonique H₂ (27-dim, irréductible sous
G2) apparaît SCINDÉ en 6 + 21, car cette base n'est pas orthonormée dans L²(S⁶).
La représentation est irréductible ; la base ne l'était pas. Détail au journal
docs/RESULTATS_NEGATIFS.md.

## Prédiction A (corrigée, exacte, propre à la sphère)
Pour des données uniformes sur S⁶, le spectre de covariance des features de degré ≤ 2
a EXACTEMENT quatre niveaux rationnels :
1/7 (×7 : H₁) ; 2/63 (×6 : diagonale sans trace de H₂) ; 1/63 (×21 : croisés de H₂) ;
0 (×1 : direction trace, x·x = 1).
Vérifié numériquement à 4 décimales (n = 60 000) ; `matches_s6_profile` teste le
profil et rejette la gaussienne. Dérivation : moments de la sphère
E[x_i²] = 1/7, E[x_i⁴] = 3/63, E[x_i²x_j²] = 1/63.

## Prédiction B (le vrai énoncé « multiplets ») — lemme de Schur
Dans une base ORTHONORMÉE d'harmoniques (`harmonic_features_on` : 7 + 6 + 21 = 34
features ON), toute mesure O(7)-invariante donne une covariance scalaire PAR BLOC :
c₁·I₇ sur H₁ et c₂·I₂₇ sur H₂ — là, la 27 est réunifiée. `schur_block_scores` mesure
l'écart au scalaire par bloc : ~0 pour S⁶ isotrope, grand sous déformation anisotrope
(testé). Raffinement futur : sous dynamique su(3) stricte (non G2), branchement
7 → 1 ⊕ 3 ⊕ 3̄ et 27 → 1 ⊕ 3 ⊕ 3̄ ⊕ 6 ⊕ 6̄ ⊕ 8 — scissions supplémentaires prédites.

## Limites assumées
Le mélange linéaire de mesure (réaliste) détruit l'invariance O(7) → le test de Schur
exige un alignement/whitening préalable (lié à la loi-pont, docs/02). Le profil exact A
suppose la mesure uniforme — sur données réelles, c'est un idéal de référence, pas une
attente ferme. Structure fine = prédiction risquée, exploratoire (prereg v2).

## Côté algèbre (durci par l'audit)
`tpl.utils.g2` : dérivations vérifiées par la propriété de LEIBNIZ D(ab)=D(a)b+aD(b)
(4×10⁻¹⁵), dim g2 = 14, su(3) = stabilisateur de e7, dim 8, FERMÉE sous crochet
(4×10⁻¹⁶). Octonions : division normée ET alternativité testées.
