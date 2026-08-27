# Chantier 5 — Protocole : tester la non-associativité

**Statut : expérience à faire. Intestable sur données passives, par
principe.** Ce fichier est le cahier qu'un labo peut exécuter. Il ne
promesse pas un résultat. Il ne réécrit pas H1 (déjà réfutée sur
Neuropixels public).

Idée : si une multiplication octonionique *effective* existait sur le
vecteur de population, la composition de trois perturbations dépendrait
du parenthésage : (A∘B)∘C ≠ A∘(B∘C). Les phases (mod 2π) sont un groupe
abélien : un test de « fermeture en triplets » sur des angles **n'est
pas** ce protocole (docs/03).

Loi-pont : A, B, C sont des déplacements du vecteur de comptages dans
R^N, pas des éléments d'une base d'octonions (docs/02). Sans une
procédure qui distingue « associateur algébrique » de « non-linéaire
banal », l'expérience reste une métaphore.

## Hypothèses (figées ici)

- H5-TPL : la divergence des trajectoires post-triplet est plus grande
  entre parenthésages que entre deux répétitions du même parenthésage,
  après égalisation des délais totaux A→C.
- H5-0 : un GLM / RNN entraîné sur les réponses *simples* (A seul, B
  seul, C seul) prédit les deux parenthésages aussi mal ou aussi bien
  l'un que l'autre (associateur compatible avec la non-linéarité déjà
  vue en uns et deux pulses).

Si H5-0 n'est pas rejetée, H5-TPL est non-discriminante. C'est le
critère d'arrêt, pas un seuil à baisser.

## Préparation (animal ou humain)

| | Souris (optogénétique, 3 aires) | Humain (TMS 3 coils) |
|---|---|---|
| Sites | 3 aires corticales distinctes, N ≥ 7 units good / aire si Neuropixels | 3 cibles ≥ 2 cm, neuronavigation |
| N | 12 animaux, même règle d'exclusion | 24 volontaires, prereg éthique à part |
| Contrôle | shuffle des identités A/B/C | sham coil + ordre des sites permuté |

Les effectifs sont un plancher de logistique, **pas** un n_min TwoNN.
Le pipeline `run_id` (n ≥ 2000 à 50 ms) exige ~100 s de trace
stationnaire : un triplet TMS ne le fournit pas. **H5 n'utilise pas
`select_geometry` comme mesure primaire.**

## Stim

- Trois pulses (ou trains opto 5 ms) d'intensité calée sur la réponse
  unitaire médiane.
- Délais intra-paire Δ = 20 ms (fenêtre où la 2ᵉ réponse n'est pas
  encore rentrée à la baseline ; à mesurer sur A seul et à figer
  *avant* les triplets).
- Deux parenthésages, **même ordre A-B-C et même temps total A→C** :
  - (A puis B) puis C : C à 2Δ après A, B à Δ après A
  - A puis (B puis C) : B et C collés en fin de fenêtre, A en tête
- 80 répétitions par parenthésage, ordre aléatoire, ISI ≥ 4 s.
- Conditions de contrôle le même jour : A, B, C, AB, BC, AC.

## Mesure primaire

Sur la fenêtre 0–150 ms après le dernier pulse, vecteur de population
(même loi-pont : comptages, une aire, pas de PCA) :

θ = dist( moyenne_(AB)C , moyenne_A(BC) ) − dist( répétition 1, répétition 2 )
du même parenthésage (demi-split).

H5-TPL : θ > 0, IC95 (sous-échantillonnage d'essais, sans remise,
n_boot = 1000) exclut 0. C'est un test de détection, comme le contraste
Claar, pas une taille d'effet.

## Nuls obligatoires (règle 1)

1. GLM / Wiener sur les réponses unaires, poussé sur les triplets.
2. RNN de `tpl.nulls.rnn` calé sur les unsaires (pas un flot S⁶).
3. Surrogate : permutation des labels de parenthésage.

Si (1) ou (2) produit un θ du même ordre, le test est **non-discriminant**
et va dans `RESULTATS_NEGATIFS.md`. On ne « corrige » pas Δ.

## Exclusions (avant déblindage des parenthésages)

- Unité : déjà `good` / `label==1`. Pas de coupe taux pour faire
  apparaître θ.
- Essai : artefact TMS / mouvement. Seuil d'artefact figé sur les
  unsaires.
- Animal / sujet : < 40 triplets valides par parenthésage →
  INDÉCIDABLE, pas de pooling inter-sujets pour sauver n.

## Ce que le labo TPL-Lab fournit

Code MIT, `prereg-v1` pour toute analyse de trace longue *en plus* de
H5 (état de repos entre blocs : même règle, même refus de concaténer).
Contact : dépôt https://github.com/AxelNoun/tpl-lab — issue « chantier 5 ».
Lettre type : `docs/26-appel-labos.md`.
