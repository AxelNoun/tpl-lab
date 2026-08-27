# Appel labos — chantiers 5 et 8

TPL-Lab (https://github.com/AxelNoun/tpl-lab) a **réfuté** sur données
publiques la partie passive d'une conjecture S⁶ / G₂ (Allen 12/12,
Claar 2 animaux, IBL INDÉCIDABLE). Deux tests restent **interventionnels
ou comportementaux**. Nous ne cherchons pas un labo pour « trouver S⁶ ».
Nous cherchons un labo pour exécuter un protocole déjà écrit, y compris
si le résultat est négatif.

## Ce que nous demandons

1. **Chantier 5** (docs/05) — TMS 3 coils *ou* optogénétique 3 aires :
   l'associateur de trois perturbations sur le vecteur de population,
   contre un nul déjà non-linéaire. Mesure : divergence de trajectoires,
   pas `select_geometry` (un triplet ne fait pas n = 2000).
2. **Chantier 8** (docs/08) — jugements de similarité (16 couleurs
   Munsell, N = 30). Stress sphère vs CIELAB. Un succès sphérique ne
   restaure pas TPL.

## Ce que nous apportons

- Plan d'analyse figé (`prereg-v1`, commit `0a5e794`).
- Code MIT, loaders NWB / IBL, pipeline `run_id`.
- Engagement de publier INDÉCIDABLE et les négatifs
  (`docs/RESULTATS_NEGATIFS.md`).

## Ce que nous refusons

Retoucher un seuil, concaténer des essais courts, PCA vers 7, z-score,
« encore une souris jusqu'à S⁶ ».

Contact : ouvrir une issue GitHub « chantier 5 » ou « chantier 8 ».
Manuscrit : `paper/registered-report.md`.
