# Parcours d'intégration — rejoindre TPL-Lab

Public : niveau master (toute discipline), bonne culture scientifique générale.
Objectif : être capable de contribuer à au moins un chantier en 6 à 10 semaines,
à raison de ~5 h/semaine. Toutes les ressources sont gratuites et légales.

Deux chemins possibles :
- **Chemin minimal** (modules 0, 1, 4, 5, 8) → contribuer aux analyses et aux nuls.
- **Chemin complet** (tous les modules) → contribuer aussi à la théorie (chantiers 1, 2, 5).

Chaque module a un *livrable* : petit exercice à déposer dans `notebooks/onboarding/`.
C'est le livrable qui valide le module, pas le temps passé.

---

## Module 0 — Comprendre le projet (1 soirée)

Lire, dans l'ordre : `README.md`, `CLAUDE.md`, `docs/03-critique-tests-originaux.md`.

**Livrable** : expliquer en 10 lignes, avec ses propres mots, pourquoi la « fermeture
de phase en triplets » ne peut pas tester la non-associativité.

## Module 1 — Python scientifique (1–2 semaines, sautable si déjà acquis)

- **Scientific Python Lectures** (scipy-lectures) : chapitres NumPy, SciPy, Matplotlib.
  Gratuit en ligne, exercices inclus.
- Complément vidéo : n'importe quelle playlist « NumPy for beginners » ; le contenu
  est standard.

**Livrable** : refaire tourner `python -m tpl.demo --seed 42`, puis modifier le nombre
d'oscillateurs du Kuramoto et tracer l'effet sur la dimension estimée.

## Module 2 — Algèbre linéaire → groupes de Lie (2–3 semaines)

1. **3Blue1Brown, « Essence of Linear Algebra »** (YouTube, sous-titres FR) — intuition
   visuelle indispensable.
2. **MIT OpenCourseWare 18.06 (Gilbert Strang)** — pour consolider ; viser les cours
   sur valeurs propres, matrices orthogonales/unitaires.
3. Groupes et symétries : **Frederic Schuller, « Lectures on the Geometric Anatomy of
   Theoretical Physics »** (YouTube) — cours 1 à 8 pour variétés et groupes de Lie.
   Alternative texte : les notes de cours librement diffusées d'Alexander Kirillov Jr,
   *Introduction to Lie Groups and Lie Algebras* (chercher le PDF sur sa page
   universitaire, Stony Brook).

Ce qu'il faut retenir pour le projet : ce qu'est SU(3) (matrices unitaires 3×3 de
déterminant 1, 8 générateurs), ce qu'est une action de groupe, ce qu'est un stabilisateur.

**Livrable** : une page expliquant pourquoi « SU(3) » n'implique PAS une « symétrie
d'ordre 3 » dans un espace d'états (l'erreur de l'article source).

## Module 3 — Octonions et G2 (1 semaine, chemin complet)

- **John Baez, « The Octonions »** — arXiv:math/0105155 (aussi paru au Bulletin of the
  AMS). Lire les sections 1 et 2 seulement : construction, table de Fano,
  non-associativité, et le fait que G2 = Aut(O).
- En parallèle, lire le code `src/tpl/utils/octonions.py` et ses tests : la table de
  multiplication y est implémentée et l'associateur calculé numériquement.

**Livrable** : vérifier à la main un cas de non-associativité (e1·e2)·e3 ≠ e1·(e2·e3)
et le retrouver avec le code.

## Module 4 — Neurosciences computationnelles (2–3 semaines)

- **Neuromatch Academy — Computational Neuroscience** : tout le matériel (tutoriels,
  vidéos, notebooks) est en libre accès sur compneuro.neuromatch.io. Faire : W1D1–W1D2
  (model fitting, types de modèles) et les jours sur la réduction de dimension.
- EEG/MEG pratique : **tutoriels MNE-Python** (mne.tools) — sections « raw data »,
  filtrage, transformée de Hilbert.
- Contexte conscience : **Chalmers, « Facing Up to the Problem of Consciousness »
  (1995)** — libre sur consc.net ; et l'entrée « Consciousness » de la **Stanford
  Encyclopedia of Philosophy** (plato.stanford.edu).

**Livrable** : charger un enregistrement d'exemple MNE, extraire les phases de 3 canaux
par transformée de Hilbert, calculer la fermeture en triplets, commenter.

## Module 5 — Systèmes dynamiques et synchronisation (1–2 semaines)

- **Steven Strogatz, « Nonlinear Dynamics and Chaos »** — les cours filmés de Cornell
  sont sur YouTube (gratuits). Viser : oscillateurs, cycles limites, synchronisation.
- Le modèle de Kuramoto : Rodrigues et al., *The Kuramoto model in complex networks* —
  arXiv:1511.07139 (introduction et section 2 suffisent).

**Livrable** : dans `src/tpl/nulls/kuramoto.py`, faire varier le couplage K et tracer
la transition de synchronisation (paramètre d'ordre r en fonction de K).

## Module 6 — Topologie appliquée / TDA (1–2 semaines, chemin complet)

- **Otter et al., « A roadmap for the computation of persistent homology »** —
  arXiv:1506.08903, open access. Lire les sections introductives.
- Tutoriels de la bibliothèque **giotto-tda** (documentation officielle en ligne).

**Livrable** : calculer la persistance H0/H1 d'un cercle bruité et d'un nuage gaussien,
et expliquer la différence. Puis lire `docs/12-calibration.md` et expliquer pourquoi
b1 ne peut pas être le test principal en dimension 6. Lecture inspirante : Gardner
et al. 2022 (*Toroidal topology of population activity in grid cells*, Nature —
préprint libre sur bioRxiv).

## Module 7 — Estimation de dimension intrinsèque (3–4 jours)

- Lire `src/tpl/analysis/intrinsic_dim.py` : l'estimateur TwoNN (Facco et al. 2017,
  *Scientific Reports*, open access — « Estimating the intrinsic dimension of datasets
  by a minimal neighborhood information ») y est implémenté en ~40 lignes.
- Comprendre pourquoi une prédiction « d = 6, pas 7 » est falsifiable.

**Livrable** : générer des sphères S² à S⁸ bruitées et vérifier que l'estimateur
retrouve la bonne dimension ; identifier à partir de quel niveau de bruit il échoue.

## Module 8 — Méthode scientifique et pré-enregistrement (2–3 jours)

- **Ioannidis, « Why Most Published Research Findings Are False »** (PLoS Medicine,
  2005, open access).
- L'entrée **« Karl Popper »** de la Stanford Encyclopedia of Philosophy (sections sur
  la falsifiabilité).
- Parcourir les gabarits de pré-enregistrement de l'**OSF** (osf.io).

**Livrable** : relire `PREREGISTRATION.md` (statut FIGÉ, tag `prereg-v1`) et
expliquer en une page pourquoi un seuil, une fenêtre ou un filtre ne se retouche
plus après le tag. Ne pas proposer de retuning.

---

## Après le parcours

Choisir un chantier dans `docs/ETAT.md` et se signaler. Bons points d'entrée :
- IBL VISp est **INDÉCIDABLE** en spontané et en session continue (docs/18–19) ;
  ne pas desserrer le seuil d'autocorrélation 0,1.
- Nul RNN à rang faible *structuré* (Mastrogiuseppe & Ostojic) : U,V indépendants
  et UUᵀ ont déjà été mesurés et écartés.
- H1-spontané Allen est déjà réfuté 12/12 (docs/14–16) ; ne pas retoucher un seuil.

## Règles de la maison (rappel)

Un nul battu, un seed fixé, un vocabulaire prudent. Le reste est dans `CLAUDE.md`.
