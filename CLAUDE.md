# CLAUDE.md — Règles du projet TPL-Lab

## Contexte

Ce projet teste rigoureusement une hypothèse inspirée de la théorie « VSA-TOE / Topological
Phase-Locking » (TPL) : *la dynamique corticale pendant une expérience perceptive soutenue
serait contrainte à une variété de basse dimension liée à SU(3) ⊂ G2 (sphère S⁶)*.

Nous ne cherchons PAS à prouver la théorie. Nous cherchons à la rendre falsifiable,
puis à la confronter aux données. Un résultat négatif propre est un succès du projet.

Les 8 chantiers sont décrits dans `README.md`. L'état d'avancement est dans `docs/ETAT.md`.

## Règles scientifiques — NON NÉGOCIABLES

1. **Toute signature doit battre un modèle nul.** Aucune analyse ne conclut « compatible
   avec TPL » sans comparaison quantitative avec au moins un nul de `src/tpl/nulls/`
   (Kuramoto, surrogates à phase randomisée). Si le nul produit la même signature,
   le test est déclaré non-discriminant et documenté comme tel.
2. **Pré-enregistrement avant données réelles.** Les seuils, statistiques et critères de
   réfutation sont figés dans `PREREGISTRATION.md` AVANT tout contact avec des données
   réelles. Interdiction de modifier un seuil après avoir vu les résultats (pas de HARKing).
3. **Synthétique ≠ réel.** Tout fichier, figure ou résultat issu de simulation porte le
   préfixe `synth_`. Ne jamais présenter une validation sur données synthétiques comme
   une confirmation empirique.
4. **Reproductibilité.** Chaque script accepte `--seed` et l'affiche. Chaque figure est
   régénérable par une commande unique documentée.
5. **Vocabulaire.** « Compatible avec » ≠ « démontre ». « Signature » ≠ « preuve ».
   Bannir « prouve que » dans les docs et messages de commit.
6. **Résultats négatifs conservés.** Un test qui échoue est documenté dans
   `docs/RESULTATS_NEGATIFS.md`, jamais supprimé.

## Faits mathématiques déjà établis (ne pas re-débattre, sourcer si besoin)

- SU(3) est le stabilisateur d'un point pour l'action de G2 sur S⁶ ; G2/SU(3) ≅ S⁶.
- Les phases (mod 2π) forment un groupe abélien : la « fermeture de phase en triplets »
  ne peut PAS tester la non-associativité octonionique. Voir `docs/03-critique-tests-originaux.md`.
- Si θ_ab := θ_a − θ_b, alors θ_ab + θ_bc + θ_ca ≡ 0 identiquement : la signature n°1
  de l'article source est algébriquement triviale telle qu'énoncée.
- Prédiction rigide retenue (chantier 6) : dimension intrinsèque de la variété neurale
  saturant à 6 (S⁶) ou 8 (dim SU(3)) — un entier prédit à l'avance, pas 7, pas 11.
- dim g2 = 14 et dim su(3) = 8 : vérifiés numériquement depuis la table octonionique
  (tpl/utils/g2.py, testé). Ne pas re-débattre.
- b1 direct : puissance nulle pour d ≥ 3 à n ≤ 3000 (docs/12). Mesures primaires
  sur données réelles : rank_candidates (chantier 9) + contrast (chantier 11).
- Spectre S⁶ (chantier 10, corrigé audit v1) : 4 niveaux EXACTS 1/7(×7), 2/63(×6),
  1/63(×21), 0(×1) en base brute — la 27 de G2 y est scindée 6+21 (base non-ON) ;
  elle se réunifie en base orthonormée (Schur). Ne plus écrire « plateau de 27 ».

## Conventions de code

- Python ≥ 3.11, numpy/scipy uniquement pour le cœur ; dépendances lourdes (giotto-tda,
  MNE) isolées dans `requirements-optional.txt`.
- Code et docstrings en anglais ; documentation `docs/` en français.
- Tests pytest obligatoires pour tout module de `src/tpl/`. Lancer : `pytest -q`.
- Style : `ruff format` avant commit. Pas de notebook dans `src/` (les notebooks vont
  dans `notebooks/` et ne contiennent aucune logique non testée).
- Les données brutes ne sont JAMAIS commitées. `data/` est gitignoré sauf `data/README.md`.

## Ce que Claude ne doit pas faire

- Ne pas ajuster un seuil, une fenêtre ou un filtre pour « faire apparaître » un effet.
- Ne pas générer de données synthétiques et les placer dans `data/` sans préfixe `synth_`.
- Ne pas citer l'article Substack source comme référence scientifique ; il est le point
  de départ à tester, pas une source. Les références valides sont dans `docs/onboarding/RESSOURCES.md`.
- Ne pas promettre de résultat sur le chantier 5 (non-associativité) : il exige des
  perturbations causales (TMS/optogénétique) impossibles avec des données passives.

## Fichiers Cursor
`.cursor/rules/*.mdc` et `.cursorrules` dupliquent ces règles pour Cursor ; en cas
de divergence, CLAUDE.md fait foi — mettre à jour les trois ensemble.

## Commandes utiles

```bash
pip install -e ".[dev]"        # installation
pytest -q                      # tests
python -m tpl.demo --seed 42   # pipeline complet sur synthétique
```

## Qui fait quoi

- Analyses & théorie : voir `docs/ETAT.md` (tableau des chantiers 1→8).
- Nouveaux contributeurs : commencer par `docs/onboarding/PARCOURS.md`.
