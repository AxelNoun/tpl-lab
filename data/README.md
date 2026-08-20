# Données
Rien n'est commité ici. Préfixe obligatoire `synth_` pour tout fichier simulé.

Jeux visés, par ordre de priorité du prereg :
1. **Allen Brain Observatory — Visual Coding Neuropixels** (éveillé seulement).
   Loader : `python -m tpl.io.allen --manifest data/allen/manifest.json ...`
   Voir `docs/13-donnees-reelles.md` pour le constat de puissance (un percept de
   10 s n'est pas puissant ; pas de concaténation d'essais).
2. **IBL Brain-wide Map** — pas de loader encore.
3. **Contraste veille / anesthésie** — pas de jeu spike public branché ; l'EEG
   OpenNeuro n'est pas l'observable de la loi-pont (docs/02).
