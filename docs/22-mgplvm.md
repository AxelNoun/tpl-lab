# 22 — Preuve géodésique-GP (stand-in mGPLVM)

Secondaire. Ne remplace pas `select_geometry`. Ne retouche pas `MAX_FIT_SCORE = 3,0`.

## Ce que c'est

Jensen et al. 2020 (*Manifold GPLVMs…*) comparent Sⁿ / Tⁿ / Rⁿ par une
vraisemblance marginale, pas par une distance de Wasserstein. Le cœur du labo
reste numpy/scipy : `tpl.analysis.manifold_evidence` est un **GP à noyau
géodésique** sur des latents MDS gelés, pas l'ELBO variationnel pytorch.

Une lecture aléatoire y = Xw ; latents = MDS du sous-échantillon projeté sur
S⁶ (normalisation R⁷), T⁶ (6 cercles appariés dans R¹²) ou R⁶ ; grille de
longueur de corrélation ; log-vraisemblance GP. `select_evidence` classe,
il ne tranche pas H1.

## Ce que ça discrimine (synth_, seed 1/2/0, n_sub=250)

| Générateur | Gagnant |
|---|---|
| S⁶ bruit 0,02 | **S⁶** |
| T⁶ plat | R⁶ (pas S⁶) |
| R⁶ | R⁶ |
| Kuramoto (sin θ) | R⁶ |

Le nul du projet n'obtient pas S⁶ (règle 1). Un vrai échantillon sphérique
est nommé S⁶.

## Résultat négatif (à garder)

Le noyau géodésique **isotrope** sur T⁶ ne récupère pas l'immersion produit
`(cos θ, sin θ)` du générateur `torus_flat`, même avec les vrais angles. Un
RBF euclidien sur le MDS 6D gagne. Ce n'est pas un permis de « forcer T⁶ ».
L'identification T⁶ vs R⁶ reste le fingerprint de `rank_candidates`
(docs/09). Un mGPLVM variationnel (extra pytorch) n'est toujours pas là ;
s'il arrive, il reste secondaire. `map_evidence` (MAP stochastique des
latents projetés sur la variété) est le stand-in numpy : toujours
secondaire, toujours pas H1. Sur un vrai S⁶ il peut nommer R⁶ (noyau
euclidien plus souple) : on ne s'en sert pas pour restaurer TPL. T⁶
toujours non récupéré.

## Contraste dégénéré (leçon Claar)

`contrast()` refuse l'IC si la fraction de lignes distinctes d'un nuage
est < 0,2 (`UNIQUE_FRAC_MIN`). n_boot du prereg inchangé. Ce n'est pas un
seuil scientifique de H1 : c'est un garde-fou de validité (docs/21, ~92 %
de doublons isoflurane). On ne jette pas les doublons pour inventer un IC.

## Sur extraits déjà mesurés (secondaire, seed 42, n_sub=300)

Pas une nouvelle H1. `select_geometry` a déjà refusé S⁶.

| Série | GP géodésique |
|---|---|
| Claar veille PL `real_claar_wake.npy` | **R6** (R6=341, S6=190, T6=−208) |
| Allen VISp `real_VISp.npy` | **R6** (R6=339, S6=197, T6=−213) |

Le GP ne restaure pas H1. Il ne nomme pas S⁶ là où le fingerprint
avait déjà dit « aucune ».

