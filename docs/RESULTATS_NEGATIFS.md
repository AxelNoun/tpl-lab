# Résultats négatifs (journal)
- [date init] Signature « triplets » : triviale ou non-discriminante (voir docs/03,
  démontré par tpl.demo). Statut : test abandonné comme discriminant.
- [calibration v1] Détection directe de b1 : puissance nulle dès d=3 à n≤1500
  (0 faux positifs). La topologie directe ne peut PAS être le test principal en dim 6
  à n réaliste. Voir docs/12-calibration.md.
- [fingerprint H1 seul] En dim 6, les distributions de persistances H1 de S⁶ et T⁶
  sont indistinguables à n=2000 — c'est la distribution des distances par paires qui
  porte la discrimination dans le fingerprint.
- [audit v1] ERREUR DE DOC CORRIGÉE : « plateaux 7 puis 27 » était faux en base brute ;
  spectre réel à 4 niveaux exacts 1/7(×7), 2/63(×6), 1/63(×21), 0(×1) — la 27 de G2
  scindée 6+21 par non-orthonormalité de la base, pas par la représentation. Corrigé :
  prédiction A (profil exact) + prédiction B (Schur en base ON, où la 27 se réunifie).
- [audit v1] multiplet_gap_score v1 (groups=(7,27)) donnait 0,77-0,92 SANS détecter la
  scission — score trompeur, remplacé par matches_s6_profile + schur_block_scores.
- [audit v1] Vérifications ajoutées qui manquaient : Leibniz des dérivations,
  fermeture de su(3) sous crochet, alternativité des octonions, TwoNN sur S²/S⁴,
  sens du couplage Kuramoto (r=0,97 à K=2 vs 0,27 à K=0).

## Audit v2

### Corrigé
- [audit v2] BUG : `contrast()` rééchantillonnait AVEC remise. TwoNN étant un estimateur
  k-NN, les duplicats gonflaient l'ID de 5,95 à 9,02 sur un vrai d = 6. Mécanisme : les
  voisins d'un point dupliqué voient µ = r₂/r₁ = 1 exactement ; log µ = 0 n'apporte rien à
  la régression mais consomme quand même un rang dans la CDF empirique, ce qui gonfle F
  de tous les autres points. Correctif : sous-échantillonnage SANS remise (m parmi n,
  frac 0,632) et dédoublonnage explicite dans `twonn()` avec avertissement — ce dernier
  protège aussi le réel (fenêtres identiques, comptages tout à zéro). Le delta ID simulé
  veille/anesthésie passe de 4,79 (faux) à 3,23, cohérent avec 6 − 3.
- [audit v2] BUG : l'« IC95 » était calculé sur 5 tirages, donc réduit au min et au max.
  Il sautait de (3,12 ; 4,38) à (4,07 ; 6,24) selon la seule graine de rééchantillonnage.
  `n_boot` par défaut porté à 1000, avertissement en dessous de 200 ; `delta_id` est
  désormais l'estimation ponctuelle sur échantillon complet. L'intervalle est déclaré
  conservateur (calculé à m < n) et non recentré.
- [audit v2] BUG : `fingerprint()` prenait les persistances H1 sur points bruts alors que
  `betti1()` rescalait. Les mêmes données dans d'autres unités marquaient 5,04 contre
  elles-mêmes au lieu de 0, et le candidat R6 (|x| moyen 0,86) était comparé à S6/T6
  (1,00) en partie sur l'échelle. Correctif : `rescale_to_unit()` en tête de
  `fingerprint()`. Score nul à 10⁻¹⁶ près sous changement d'échelle.

- [audit v2] BUG : `rank_candidates` ne pouvait pas répondre « aucun des trois » — des
  données S³ étaient déclarées R6, un bruit gaussien 20-D était déclaré T6, et la mesure
  primaire n°1 partait donc d'une chance de base de 1/3. Correctif : `select_geometry()`
  applique un seuil d'adéquation absolu `MAX_FIT_SCORE = 3,0`, calibré sur synthétique
  avant toute donnée réelle et reproductible par
  `python -m tpl.analysis.calibration --fit-threshold`. Marge de séparation mesurée
  [2,56 ; 4,05] : 0 % de faux positifs, 0 % de faux négatifs, et le nul de Kuramoto du
  projet est rejeté (4,20 à K=0, 29,05 à K=2), donc la règle 1 est satisfaite. Branché
  sur `state_contrast.metrics_for` : l'« anesthésie » simulée renvoie désormais
  `best_geometry = None` (score 18,72) au lieu d'un R6 nommé par défaut. Limite déclarée
  dans docs/09 : un vrai S⁶ à bruit ≥ 0,15 est rejeté lui aussi — le test perd sa
  puissance, il ne se trompe pas.

### Mesuré, non corrigé — à traiter avant de figer le prereg
- [audit v2] Le pipeline pré-enregistré n'existe pas : ni `tpl.analysis.run_id` ni
  `configs/prereg_v1.yaml`. La décimation « autocorrélation < 0,1 » n'est pas implémentée
  (la démo code en dur `[::10]`) ; sur un vrai d = 6, les facteurs voisins donnent 5,59 à
  6,54, soit toute la fenêtre ±0,5 et au-delà. C'est exactement le degré de liberté que la
  règle 2 de CLAUDE.md interdit.
- [audit v2] Critères de réfutation incomplets : ID < 5,5 n'est ni une confirmation ni une
  réfutation, et 6,5 comme 7,5 appartiennent à la fois à une fenêtre d'acceptation et à
  l'intervalle de réfutation.
- [audit v2] b1 direct meurt dès d = 3 (T³ : 0 détection sur 30 à n = 2000), pas d = 4
  comme l'annonce la docstring de `calibration.py` ; docs/12 avait raison. La
  conservativité tient : 0 faux positif sur 180 essais.
- [audit v2] TwoNN converge vers d PAR EN DESSOUS : 5,74 à n=250 ; 5,82 à n=1000 ; 5,97 à
  n=16000 pour un vrai 6. À n ≤ 500 le plancher 5,5 du prereg est à moins d'un écart-type,
  d'où un risque de réfuter à tort. Fixer un n minimal avant de figer.

### Revérifié indépendamment et correct
- [audit v2] Table octonionique (Moufang 2,8×10⁻¹⁴, alternativité 1,1×10⁻¹⁴) ; Leibniz sur
  les 21 paires de générateurs et pas seulement 3 (7,1×10⁻¹⁵) ; dim g2 = 14 avec éléments
  antisymétriques ; su(3) confirmée par forme de Killing définie négative (valeurs propres
  toutes à −3,00 : compacte et simple, et la seule algèbre simple compacte de dimension 8
  est su(3)) ; spectre S⁶ redérivé à la main depuis les moments de la sphère puis vérifié à
  n = 60 000 ; base harmonique orthonormée 7+27 (covariance → I₃₄, écart max 0,0096, le QR
  sur matrice de rang déficient est correct). Le classement est aussi robuste au décalage
  de n (candidats figés à 2000, données de 300 à 10 000 : toujours S6) et généralise à un
  S⁶ échantillonné autrement que par le générateur candidat — la validation « acc 1,0 »
  n'est donc pas purement circulaire.
