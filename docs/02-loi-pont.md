# Chantier 2 — La loi-pont

Sans dictionnaire explicite mesure ↔ géométrie, H-TPL ne prédit rien. Le critère
d'acceptation n'a pas changé : chaque ligne spécifie une procédure d'estimation
dans `src/tpl/` et une unité. Une ligne sans procédure n'est pas une prédiction
en attente — c'est l'absence de prédiction.

## Ce qui est figé (ligne 1)

| Élément géométrique | Grandeur neurale | Échelle | Unité | Procédure |
|---|---|---|---|---|
| Point de la variété hypothétique | vecteur de comptage de spikes, fenêtre 50 ms non chevauchante, **tous** les unités d'**une** aire qui ont spiké au moins une fois | une aire corticale à la fois (Allen : V1, LM, AL, … séparément) | spikes / 50 ms | `tpl.analysis.bridge.bin_population` → `prepare_population` → `run_id` |

Le nuage analysé vit dans R^N, N = nombre d'unités actives, N ≥ 7. Ce n'est **pas**
un point de S⁶ ⊂ R⁷. L'hypothèse porte sur la géométrie *intrinsèque* de la
trajectoire, pas sur l'existence d'une base à 7 électrodes. TwoNN et
`select_geometry` travaillent dans l'espace ambiant ; ils n'ont pas besoin d'une
réduction.

### Ce que la procédure refuse, et pourquoi

Le risque principal du gabarit v1 était « réduit à R⁷ » : un PCA à 7 composantes
plafonne la dimension ambiante à 7 et peut fabriquer d̂ ≤ 7. C'est exactement le
degré de liberté que la règle 2 de CLAUDE.md interdit. Figé :

- **pas de PCA, NMF, ni projection apprise vers 7 ou 8 dimensions**
- **pas de z-score ni de racine carrée par canal** — TwoNN n'est pas invariant
  aux dilatations anisotropes ; égaliser les variances « sphériserait » le nuage
  vers S⁶
- **pas de seuil de taux de décharge** au-delà de « au moins un spike » — couper
  à 0,5 Hz ou 2 Hz est un bouton d'HARKing classique
- **pas de fusion d'aires** — mélanger V1 et LM mélange deux variétés
- **fenêtre = 50 ms, non chevauchante** — déjà dans `configs/prereg_v1.json` ;
  `bin_population` refuse toute autre durée

Le risque déclaré de ce choix : les unités à haut taux dominent les distances
euclidiennes. C'est accepté. Une analyse de sensibilité (z-score, racine) pourra
être publiée comme telle ; elle ne peut pas changer le verdict primaire.

Le modèle d'observation du génératif (`s6_flow.observe` : mélange linéaire +
bruit) est la raison pour laquelle on n'inverse pas M. Tester le nuage observé,
pas un latents reconstruit.

## Ce qui n'est pas une prédiction (lignes 2 et 3)

| Élément géométrique | Pourquoi il n'y a pas de procédure | Conséquence |
|---|---|---|
| Action de SU(3) | Une action est une *famille* de transformations. Observer une trajectoire sur une variété ne dit pas quel groupe agit. Distinguer SO(7) (rotations génériques, déjà dans `simulate_s6`) de SU(3) (stabilisateur d'un point) exige soit l'holonomie de lacets, soit une intervention. Le génératif `simulate_su3_flow` ajoute d'ailleurs un bruit *transverse* aux orbites su(3) pour couvrir S⁶ : même le synthétique n'est pas une orbite SU(3) pure. | **Pas de prédiction** sur données passives. |
| Multiplication octonionique | Composer deux perturbations causales. Intestable par principe sur de l'observation (docs/05). Sans identifier A, B, C à des éléments d'une base d'octonions — ce que la ligne 1 refuse explicitement — le protocole dit *quoi* on compose (des déplacements du vecteur de population dans R^N) mais pas comment reconnaître une structure octonionique plutôt qu'une non-linéarité banale. | **Pas de prédiction.** Le chantier 5 reste un protocole, pas un test. |

Nommer « bande thêta » ou « rotations de l'espace des phases » à la place d'une
procédure serait de la spéculation ajustable aux données. Le gabarit l'interdit.

## Conséquence sur la prédiction spectrale (chantier 10)

Les prédictions A et B (niveaux 1/7, 2/63, 1/63, 0 ; multiplets de Schur) sont
des énoncés sur S⁶ ⊂ R⁷ en coordonnées. Le mélange linéaire réaliste détruit
l'invariance O(7) (docs/10, déjà écrit). `refuse_reduction` interdit de
fabriquer ces coordonnées par PCA : `covariance_spectrum` et
`harmonic_features_on` lèvent une erreur si l'ambiant n'est pas 7.

**Sur Neuropixels, la prédiction spectrale n'est donc pas applicable.** Elle
reste un test de cohérence du génératif synthétique, déclarée exploratoire dans
le prereg, et désormais inapplicable aux enregistrements mélangés plutôt que
« en attente d'un alignement ». C'est un résultat négatif de la loi-pont, pas un
détail d'implémentation.

## Ce que H-TPL prédit réellement, une fois la loi-pont écrite

Sur le vecteur de population d'une aire, fenêtres de 50 ms, décimé jusqu'à
autocorrélation < 0,1, n ≥ 2000 après décimation :

1. dimension intrinsèque dans [5,5 ; 6,5[ ou [7,5 ; 8,5[
2. ET `select_geometry` accepte S⁶ (score ≤ 3,0)
3. ET ces deux mesures s'effondrent sous anesthésie (contraste, docs/11)

Tout le reste — SU(3), octonions, multiplets 7/27 sur du réel — n'a pas de
loi-pont, donc n'est pas dans H1.
