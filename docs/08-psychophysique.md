# Chantier 8 — Psychophysique structurelle (protocole)

On renonce à « résoudre » le problème difficile. Version testable :

> La métrique de similarité perceptive (jugements humains) est-elle mieux
> décrite par une sphère que par l'alternative forte (CIELAB / euclidien) ?

**Prémisse morte.** L'énoncé d'origine (« isomorphe à la variété neurale
du chantier 6 ») suppose un S⁶ neural. H1-spontané est réfuté 12/12 et
le contraste Claar aussi. On ne recycle pas des jugements de couleur
pour restaurer TPL. Le test ci-dessous est **indépendant** du cortex : un
succès sphérique ne sauve pas Allen ; un succès CIELAB ne dit rien de
plus que ce que la psychophysique de la couleur sait déjà.

## Hypothèses

- H8-sphère : après MDS, le stress de la projection sur la sphère unité
  est inférieur au stress euclidien (et au stress d'un plongement CIELAB
  3D si les stimuli sont des couleurs).
- H8-0 : CIELAB (couleurs) ou l'euclidien (timbres) gagne ou égale.

Réfutation de « TPL apporte quelque chose ici » : H8-0 n'est pas rejetée.
Outil : `tpl.analysis.psychophysics.rival_fit`.

S⁶ neural n'est **pas** la mesure. 12–24 stimuli ne portent pas une
6-sphère. On embarque en 3D (couleur) ou 4D (timbre), pas en 7.

## Stimuli

- Couleurs : 16 Munsell, illuminant D65, écran calibré. Paire à paire
  (120 paires), Likert 0–8 « dissimilaires », 3 répétitions.
- Timbres (option) : 12 sons harmoniques, même protocole. Nul : MFCC
  euclidien, pas CIELAB.
- N = 30 observateurs naïfs, écrit **avant** le premier jugement.
  Exclusion : daltonisme (Ishihara) pour la branche couleur ; < 80 % de
  paires complètes → INDÉCIDABLE individuel, conservé dans le n agrégé
  seulement si ≥ 24 complets.

## Analyse (pas de HARKing)

```bash
python -m tpl.analysis.psychophysics --synthetic --seed 42
python -m tpl.analysis.psychophysics --ratings data/real_similarity.npy --seed 42
```

```python
from tpl.analysis.psychophysics import dissimilarity_from_ratings, rival_fit
fit = rival_fit(D, seed=42)
```

- Matrice : moyenne des répétitions, symétrisée.
- Stress euclidien 3D vs sphère (même 3D, rayon 1).
- Seed 42. Pas de retrait de stimuli « mal placés » après coup.
- Inférence : bootstrap des observateurs (n_boot = 1000, sans remise,
  frac 0.632) sur `stress_euclidean - stress_sphere`. IC qui exclut 0
  dans le sens sphère = H8-sphère ; sinon H8-0.

`select_geometry` n'est appelé que si n_stim ≥ 20, et son verdict n'est
**pas** H8. C'est une étiquette secondaire, comme le GP géodésique.

## Ce que ça n'est pas

Pas un substitut de H1. Pas une raison d'aller chercher une 13ᵉ aire
Allen. Pas un test d'octonions.
