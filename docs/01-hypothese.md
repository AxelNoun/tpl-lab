# Chantier 1 — L'hypothèse locale (l'amputation)

On abandonne toute prétention de « théorie du tout ». Après loi-pont, nuls, et
calibration, la partie *testable sur données passives* tient en une phrase :

> **H-TPL (empirique)** : le nuage de vecteurs de population d'**une** aire
> corticale, comptages de spikes en fenêtres de 50 ms, a une dimension
> intrinsèque dans `[5,5 ; 6,5[` **et** est classé S⁶ par `select_geometry`
> (score ≤ 3,0), pas T⁶, pas R⁶, pas « aucun candidat ».

Ce n'est pas la phrase du gabarit v1. Le gabarit disait aussi « difféomorphe à
S⁶ ≅ G2/SU(3) » et « la dynamique commute avec une action de SU(3) ». Ni
l'isomorphisme G2/SU(3), ni l'action, n'ont de procédure d'estimation sur une
trajectoire observée (docs/02). Les garder dans H1, c'est affirmer ce qu'on ne
teste pas.

## Ce qui est testable, et ce qui ne l'est pas

| Affirmation | Statut | Pourquoi |
|---|---|---|
| ID ∈ [5,5 ; 6,5[ ou [7,5 ; 8,5[ | testable, primaire | TwoNN, n ≥ 2000 après décimation |
| géométrie = S⁶ (pas T⁶, pas R⁶) | testable, primaire | `select_geometry`, seuil 3,0 |
| les deux s'effondrent sous anesthésie | testable **si** un jeu spike existe | `contrast` ; Allen n'en a pas |
| b1 = 0 | non discriminant à d ≥ 3 | puissance nulle, 0 faux positif |
| multiplets 1/7, 2/63, 1/63 | inapplicable au réel N-canaux | énoncé sur S⁶ ⊂ R⁷ ; PCA interdit |
| action de SU(3) | pas une prédiction | une action n'est pas une trajectoire |
| multiplication octonionique | pas une prédiction | interventionnel, et sans base d'octonions |
| percept soutenu > 10 s | non puissant sur Neuropixels public | 10 s = 200 fenêtres ; il en faut 2000 |

## Inférence forte (ce qui reste)

La question n'est pas « TPL est-elle vraie ? ». C'est : parmi {S⁶, T⁶, R⁶, aucune},
laquelle décrit le nuage ? H-TPL est le cas S⁶. Un T⁶ ou R⁶ qui passe le seuil
est une *découverte contre* TPL, pas une confirmation molle.

Le premier test empirique déclaré (docs/13) est encore plus faible : un bloc
`spontaneous` Allen, éveillé, sans percept contrôlé. Un compatible là n'autorise
pas à parler de perception. Un réfutant là réfute aussi la version perceptive.

## Vocabulaire

« Compatible avec S⁶ » ≠ « démontre G2 ». Même un S⁶ confirmé peut venir d'autre
chose que des octonions. Bannir « prouve que ».
