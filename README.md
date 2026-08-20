# TPL-Lab — Falsifier la « géométrie de la conscience »

Un laboratoire computationnel pour transformer la conjecture VSA-TOE / Topological
Phase-Locking (une théorie spéculative publiée sur Substack) en hypothèse scientifique
testable — et la tester honnêtement.

**Hypothèse de travail (H1)** : pendant une perception soutenue, la dynamique de
population neuronale est confinée à une variété de basse dimension héritée de la
géométrie G2/SU(3) ≅ S⁶, avec une dimension intrinsèque prédite de **6** (ou 8).

**Hypothèse nulle (H0)** : la dynamique est celle d'oscillateurs couplés génériques
(Kuramoto, réseaux récurrents), sans structure octonionique — et reproduit déjà toutes
les « signatures » proposées par l'article d'origine.

## Les 12 chantiers

| # | Chantier | Statut | Où |
|---|----------|--------|-----|
| 1 | Hypothèse locale formelle (amputer la TOE) | ✅ rédigé | `docs/01-hypothese.md` |
| 2 | Loi-pont (neurones → variété) | 🟡 gabarit | `docs/02-loi-pont.md` |
| 3 | Modèle génératif S⁶ + projection réaliste | 🟡 squelette fonctionnel | `src/tpl/generative/` |
| 4 | Modèles nuls (Kuramoto, surrogates) | 🟡 squelette fonctionnel | `src/tpl/nulls/` |
| 5 | Test de non-associativité (interventionnel) | 🔴 protocole seul — exige un labo | `docs/05-protocole-non-associativite.md` |
| 6 | Dimension intrinsèque = 6 ou 8 (prédiction rigide) | 🟡 pipeline prêt pour données réelles | `src/tpl/analysis/` |
| 7 | Pré-enregistrement | 🟡 pipeline exécutable, à figer | `PREREGISTRATION.md`, `src/tpl/analysis/run_id.py` |
| 8 | Psychophysique structurelle | 🔴 protocole seul | `docs/08-psychophysique.md` |
| 9 | Ranking de géométries (S⁶/T⁶/R⁶) | ✅ acc 1,0 synthétique | `docs/09-geometries-candidates.md` |
| 10 | Multiplets G2 ; g2/su(3) numériques | ✅ validé | `docs/10-multiplets-spectraux.md` |
| 11 | Contraste d'états (benchmark PCI) | 🟡 outil prêt | `docs/11-contraste-etats.md` |
| 12 | Calibration / puissance | 🟡 v1 (résultat clé) | `docs/12-calibration.md` |

Premier résultat du projet (déjà acquis, voir `docs/03-critique-tests-originaux.md`) :
la signature n°1 de l'article source (fermeture de phase en triplets) est soit
algébriquement triviale, soit reproduite par un Kuramoto banal. Elle ne teste rien
d'octonionique. La démo le montre en 30 secondes.

## Quick start (5 minutes)

```bash
git init tpl-lab && cd tpl-lab   # ou dézipper l'archive ici
pip install -e ".[dev]"
pytest -q                        # tout doit passer
python -m tpl.demo --seed 42     # démo : S⁶ synthétique vs Kuramoto
```

La démo génère une trajectoire sur S⁶, un Kuramoto, estime la dimension intrinsèque
des deux (attendu : ≈ 6 pour S⁶) et montre que la fermeture de phase en triplets ne
les distingue pas.

## Utiliser avec Cursor ou Claude Code

Les règles du projet sont dans `CLAUDE.md` (Claude Code la lit nativement) et
dupliquées pour Cursor dans `.cursor/rules/` et `.cursorrules`. Ouvrir le dossier
dans l'un ou l'autre : les règles scientifiques s'appliquent automatiquement.

## Ancienne section Claude Code

Le fichier `CLAUDE.md` contient les règles du projet (rigueur scientifique, conventions,
interdits). Ouvrir simplement Claude Code dans ce dossier : il les lit automatiquement.

## Données réelles

Aucune donnée n'est incluse. `data/README.md` liste les jeux open source visés
(Allen Brain Observatory / Neuropixels, OpenNeuro, IBL) et comment les télécharger.
Règle absolue : figer `PREREGISTRATION.md` avant la première analyse réelle.

## Rejoindre le projet

Niveau master suffisant. Parcours de mise à niveau (6–10 semaines à temps partiel,
ressources 100 % gratuites) : `docs/onboarding/PARCOURS.md`.

## Licence & esprit

MIT pour le code. L'esprit : un résultat négatif propre vaut mieux qu'une confirmation
molle. On documente ce qui échoue.
