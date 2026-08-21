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

- [audit v2] MANQUANT : le pipeline pré-enregistré n'existait pas — `PREREGISTRATION.md`
  décrivait une analyse que personne ne pouvait rejouer. Créés : `tpl/analysis/run_id.py`
  et `configs/prereg_v1.json` (JSON et non YAML : pas de dépendance hors numpy/scipy dans
  le cœur). Tout degré de liberté d'analyste est lu dans la config et réaffiché en sortie ;
  `load_config` refuse un `max_fit_score` modifié après calibration.
- [audit v2] MANQUANT : la décimation « autocorrélation < 0,1 » était annoncée mais non
  implémentée (la démo codait en dur `[::10]`). Implémentée dans
  `intrinsic_dim.decorrelate`. Sur une rotation S⁶ de vraie dimension 6, les facteurs
  choisis à la main 1 / 2 / 5 / 10 donnent 4,05 / 4,49 / 5,40 / 6,01 : l'analyste décidait
  du verdict à lui seul. **Tension résiduelle déclarée** : décimer coûte des échantillons,
  et les facteurs 50 et 100 sur la même trajectoire redescendent à 5,19 et 5,08 (n = 400 et
  200) par le biais de petit échantillon. La règle ne suffit donc pas seule — d'où le
  plancher de n ci-dessous.
- [audit v2] Critères de réfutation incomplets, corrigé : `run_id.classify_id` utilise des
  fenêtres semi-ouvertes `[t−0,5 ; t+0,5[`, exhaustives et sans recouvrement, testées à
  toutes les bornes et sur 1500 valeurs. `ID < 5,5` réfute désormais explicitement (au lieu
  de n'être ni l'un ni l'autre) et la nouvelle règle n'est plus permissive que l'ancienne
  en aucun point.
- [audit v2] TwoNN converge vers d PAR EN DESSOUS — chiffré en taux de réfutation À TORT
  d'un vrai S⁶ sous la règle du prereg (200 graines par point) : 36,5 % à n = 250 ; 17,5 %
  à n = 500 ; 14,0 % à n = 1000 ; 2,5 % à n = 1500 ; 1,0 % à n = 2000. Le plancher est fixé
  à **n = 2000 après décimation** et `run_id` renvoie INDÉCIDABLE en dessous, sans publier
  d'estimation. Conséquence expérimentale à assumer avant d'enregistrer : 45 min à 1 h 30
  de signal continu par condition.

### Nouveau — mesuré sur le pipeline lui-même
- [audit v2] NON-DISCRIMINANT : la mesure 1 seule ne bat pas le nul tant que la variante
  d = 8 est autorisée. Un Kuramoto de 12 oscillateurs, décimé par la même règle, donne
  ID = 8,23 — à l'intérieur de la fenêtre d'acceptation `[7,5 ; 8,5[`. La variante « ou
  d = 8 = dim SU(3) » double le nombre de cibles et élargit assez la zone d'acceptation
  pour qu'un oscillateur générique y tombe. Ce qui sépare, c'est la mesure 2 : le nul ne
  correspond à aucun candidat (meilleur score 55,8) là où le flot su(3) donne S⁶ à 0,47.
  Conséquence figée dans `run_id` : le verdict H1 est **conjonctif** (dimension ET
  géométrie), une compatibilité de dimension seule ne compte pas.

- [calibration] TROU dans le conjonctif : « géométrie acceptée » sans exiger le nom
  S⁶. Un R⁶ de vraie dimension 6 a l'ID dans [5,5 ; 6,5[ **100 %** du temps et passe
  `MAX_FIT_SCORE` ; l'ancienne règle l'aurait déclaré compatible avec H-TPL. Un tore
  plat T⁶ a TwoNN ~6,6 (souvent déjà hors fenêtre) mais gagne toujours le ranking T6.
  Correctif : `h1_verdict` exige `geometry == "S6"`. Mesure à n = 2000, 8 graines :
  TPR 100 % (S⁶) ; TNR 100 % (T⁶, R⁶, Kuramoto, gaussienne 20-D).
  `python -m tpl.analysis.calibration --h1-power`.

- [calibration] TPR(n) (8 graines, règle sans plancher) : à n = 500 le TPR sur un
  vrai S⁶ est 88 %, et les 12 % de ratés sont tous TwoNN (S⁶ accepté 100 %). Dès
  n = 1000 le TPR affiché est 100 %, mais 8 graines ne voient pas les 14 % de
  réfutations à tort mesurés sur 200 graines à n = 1000. Le plancher n_min = 2000
  **ne baisse pas**.
- [calibration] Bruit additif sur un vrai S⁶, n = 2000 : TPR 100 % à σ = 0,03 ;
  88 % à 0,08 ; 50 % à 0,12 ; 12 % à 0,15 ; 0 % à 0,20. Entre 0,08 et 0,12,
  TwoNN sort de la fenêtre alors que `select_geometry` accepte encore S⁶. Le
  seuil 3,0 ne devient le facteur limitant qu'à 0,15, comme calibré.

- [audit v2] NON-CORRIGEABLE PAR RÉÉCHANTILLONNAGE : l'IC95 sur delta ID n'est pas une
  taille d'effet. Mesuré par `python -m tpl.analysis.calibration --ci-coverage`, couverture
  de la vraie différence : **98 % sur un contraste 6 contre 3, mais 40 % sur 10 contre 3**
  (n = 1200). En dimension élevée le biais de TwoNN sur la différence (≈ 1,3) dépasse la
  largeur de l'intervalle (≈ 1,5), et aucun schéma de rééchantillonnage ne peut le réparer :
  le rééchantillonnage n'a pas accès au biais.
  La correction de manuel a été essayée et **rejetée sur mesure** : rescaler la racine
  θ_m − θ_n par √(m/n) (Politis & Romano 1994) est le correctif principiel d'un intervalle
  calculé à m < n, et il fait *chuter* la couverture à 65 % (32 % dans le cas 10 contre 3).
  Le biais de TwoNN bouge à peine entre m et n, donc le sous-échantillonnage ne le voit pas ;
  le rescalage supprime la seule chose qui le compensait, à savoir la largeur excédentaire.
  Ce qui survit, c'est le SIGNE : le biais croît avec d, donc la différence est SOUS-estimée
  et l'intervalle est tiré vers zéro. Le critère « IC95 excluant 0 » reste donc conservateur
  — la revendication devient plus difficile, jamais plus facile — mais la largeur ne doit
  jamais être publiée comme barre d'erreur. Prereg mesure 2 reformulée en conséquence.
- [audit v2] Même cause, symptôme visible : l'IC95 peut exclure sa propre estimation
  ponctuelle (delta = −2,27, IC [−2,18 ; −1,30] sur le dry-run) quand les deux conditions
  diffèrent beaucoup en dimension.

## Chantier 4 — le nul RNN aléatoire (nouveau)

Adversaire le plus sérieux du projet : un réseau récurrent chaotique produit une
dynamique de basse dimension sans aucune géométrie S⁶. Testé avec 200 unités,
140 000 pas, décimation par la règle du prereg (n ≈ 2200 à 2400 après décimation) :

| g | lag | n | d̂ | géométrie | score |
|---|---|---|---|---|---|
| 1,4 | 63 | 2223 | 12,40 | AUCUNE (R6) | 32,50 |
| 1,5 | 61 | 2296 | 9,59 | AUCUNE (R6) | 29,65 |
| 1,6 | 59 | 2373 | 3,44 | AUCUNE (R6) | 15,46 |
| 1,8 | plafond | 140 | — | INDÉCIDABLE | — |

- **Le nul perd sur les deux mesures**, à tous les gains testés : dimension hors
  fenêtre (12,4 / 9,6 / 3,4, jamais dans [5,5 ; 6,5[) et aucun candidat géométrique
  (scores 15 à 32 contre un seuil de 3,0). Le gain `g` ne permet pas de le régler sur
  la prédiction : d̂ varie de façon non monotone et saute par-dessus 6.
- **DÉMONSTRATION DU PLANCHER n, sur un vrai nul et non sur du S⁶ synthétique** : à
  g = 1,5, le même réseau donne d̂ = 5,24 sur 328 échantillons (donc DANS la fenêtre
  d'acceptation) mais 9,59 sur 2296. Sans le plancher n ≥ 2000, ce nul aurait produit
  une confirmation. C'est la justification la plus concrète du critère de puissance.
- **BUG TROUVÉ PAR CE TEST** : à g = 1,8 la recherche de lag atteignait son plafond
  sans que la série décorrèle jamais, et le pipeline continuait en silence — d̂ = 6,14
  sur 140 échantillons jamais indépendants, soit une confirmation fabriquée à partir
  d'autocorrélation. `autocorrelation_time` avertit désormais et `run_id` renvoie
  INDÉCIDABLE dans ce cas.
- **Deux impasses mesurées, à ne pas retenter** : `W = g·U·Vᵀ/N` à U et V indépendants
  ne produit aucune dynamique (le recouvrement u_k·v_k/N s'annule, donc pas de boucle
  de rétroaction) et donne d̂ ≈ 50-65, qui est la boule de bruit à 200 dimensions et
  non une variété ; la variante symétrique `W = g·U·Uᵀ/N` converge vers des points
  fixes, même symptôme (d̂ ≈ 58-70). Le recouvrement structuré est
  `simulate_lowrank_rnn` (docs/20).

## Nul rang faible structuré — RÉFUTÉ (21 août 2026, synth_)

`simulate_lowrank_rnn` (mode `oscillatory`, rang 6, ρ = 0,8, g = 4, 200
unités, 140 000 pas, seed 42) : n = 8236 après décimation 1/17. ID = 14,95
(hors fenêtre) ; aucun candidat (R6, score 36,76). Verdict **RÉFUTÉE**.
Le rang 6 de W n'est pas S⁶. Détail : `docs/20-nul-lowrank.md`.
La circulation pure sans gain meurt à l'origine (valeurs propres −1 ± i gρ) :
ce n'est pas un oubli, c'est le calcul.

## Contraste Claar (DANDI 000458) — H1 réfutée veille et isoflurane (21 août 2026)

`sub-551399_ses-20210128`, aire PL, 205 unités. Veille 1787 s (n = 5957) :
ID = 39,20, aucune géométrie. Isoflurane 1659 s (n = 33188) : ID = 29,64,
aucune géométrie, **92 % de fenêtres dupliquées**. Ni S⁶ en veille ni S⁶ sous
isoflurane. Le CI du contraste n_boot = 1000 n'est pas un résultat : la série
isoflurane est dégénérée. Détail : `docs/21-claar-contraste.md`.

## Preuve géodésique-GP — T⁶ non récupéré (21 août 2026, synth_)

`manifold_evidence` (stand-in mGPLVM, docs/22) nomme S⁶ sur un vrai
échantillon sphérique et ne le nomme pas sur T⁶, R⁶ ou Kuramoto. Le noyau
géodésique isotrope **ne récupère pas** l'immersion produit de `torus_flat`.
Ce n'est pas Jensen 2020. Ce n'est pas H1. On ne force pas T⁶.
Sur extraits déjà réfutés (seed 42) : Claar veille et Allen VISp sont
nommés **R6**, pas S⁶. Le GP ne restaure pas H1.

## Chantier 2 — remplir la loi-pont a rétréci H1, pas élargi

- [loi-pont] « Réduit à R⁷ » était le degré de liberté que le gabarit signalait. Il
  est gelé à OFF : PCA / z-score / seuil de taux / fusion d'aires sont refusés par
  `tpl.analysis.bridge`. Conséquence : les prédictions spectrales A/B (docs/10) sont
  des énoncés sur S⁶ ⊂ R⁷ et **ne s'appliquent pas** aux enregistrements N-canaux.
  `covariance_spectrum` lève une erreur si l'ambiant ≠ 7 au lieu de tronquer
  silencieusement le spectre à 35 valeurs. H1 empirique se réduit aux deux mesures
  primaires (dimension + géométrie du fingerprint) ; SU(3) et les octonions n'ont
  pas de procédure, donc pas de prédiction (docs/02).

## Chantier 6 — H1 « percept > 10 s » n'est pas puissant sur du Neuropixels public

- [loader] 10 s de stimulus à 50 ms = 200 fenêtres ; n_min = 2000 exige 100 s à lag 1
  et 45–90 min aux lags des flots synthétiques. Un grating Allen dure ~2 s. Cent
  repeats sommés feraient 200 s et passeraient le plancher : le loader prend la durée
  du plus long bloc continu, pas la somme (`report_power`, tests/test_extract.py).
  `extract_block` refuse < 100 s plutôt que de concaténer. Premier test déclaré :
  **H1-spontané**, plus faible que H1 (pas de percept contrôlé). Un compatible là
  n'autorise pas à parler de percept ; un réfutant là réfute aussi H1. Allen Visual
  Coding n'a pas d'anesthésie : le contraste d'états n'est pas testable sur ce jeu.

## Premier test empirique — H1-spontané RÉFUTÉ (20 août 2026)

Session Allen `767871931` (functional_connectivity), aire **VISp**, plus long
bloc `spontaneous` continu 1802,5 s (pas la somme des 6 blocs), 201 unités
`good`, fenêtres 50 ms → 36050 × 201, décimation 1/5 → n = 7210 ≥ 2000.

- mesure 1 : ID = 37,07 ≥ 8,5 → réfutée
- mesure 2 : aucun candidat (meilleur R6, score 41,68 > 3,0) → réfutée
- verdict conjonctif : **RÉFUTÉE**

Commandes et lecture : `docs/14-h1-spontane.md`. Seuils non retouchés.

Batterie supplémentaire (docs/15, déclarée avant les verdicts) : VISal, VISam,
VISpm, VISrl, VISli, même session et même bloc — **6/6 réfutées**, plus le
surrogate de phase de VISp. Aucune ne nomme S⁶. Une autre session serait un
nouveau test, pas un rattrapage.

Réplication (docs/16, session `766640955`, autre animal, déclarée avant le
NWB) : 6/6 aires `VIS*` réfutées. Deux fois S⁶ en tête du ranking (scores
26,75 et 25,50) : le cutoff 3,0 tient. Total **12/12**.

## IBL — spontaneousActivity INDÉCIDABLE (21 août 2026)

Première insertion VISp Brain-wide Map avec spontané ≥ 100 s et N ≥ 7
(`docs/17`, `docs/18`) : eid `5ae68c54-2897-4d3a-8120-426150704385`, 600,1 s,
17 good `VISp6a`. 12001 fenêtres, décimation 1/9 → **n = 1334 < 2000** →
INDÉCIDABLE. RFM / replay / essais non collés. Ne restaure pas Allen.

Session continue, même insertion (`docs/19`, déclarée avant l'extract) :
horloge 97,5 min, 117049 fenêtres, décimation 1/1000 → **n = 118**.
L'autocorrélation ne passe pas sous 0,1 en 1000 pas. Toujours INDÉCIDABLE.
Ne pas desserrer le seuil.


### Cohérence et nuls affaiblis (F9 à F14, corrigés)
- [audit v2] b1 direct meurt dès d = 3 (T³ : 0 détection sur 30 à n = 2000), pas d = 4
  comme l'annonçait la docstring de `calibration.py` ; docs/12 avait raison. Docstring
  corrigée. La conservativité tient : 0 faux positif sur 180 essais.
- [audit v2] NUL AFFAIBLI : `phase_randomize` tirait une phase indépendante PAR CANAL,
  ce qui détruisait aussi les corrélations inter-canaux. C'était donc un nul pour « tout
  couplage », pas pour « autre chose qu'un couplage linéaire » — un adversaire qu'une
  variété de basse dimension bat gratuitement, ce qui contrevient à l'esprit de la
  règle 1. Le défaut par défaut est désormais `preserve_cross=True` : une seule phase par
  fréquence, appliquée à tous les canaux, ce qui conserve l'inter-spectre. Vérifié par
  test : corrélation croisée moyenne conservée à 0,05 près, contre effondrement sous
  0,3 avec l'ancien comportement (sur signal LARGE BANDE — sur un signal bande étroite
  la démonstration est impossible dans un sens comme dans l'autre, deux phases aléatoires
  à une même fréquence donnant |corr| = |cos Δφ|, de moyenne 2/π).
  Corrigé au passage : la raie de Nyquist n'était pas forcée réelle en longueur paire,
  donc `irfft` en jetait silencieusement la partie imaginaire et le spectre de puissance
  du surrogate ne coïncidait plus avec l'original.
- [audit v2] `matches_s6_profile` exige des données de norme unité — 1/7, 2/63 et 1/63
  sont des valeurs absolues, donc un simple facteur d'échelle 2 fait échouer le test sur
  un S⁶ parfait. Précondition désormais documentée (rotations inoffensives ; passe à
  bruit 0,05, échoue à 0,10).
- [audit v2] `THEORY_S6` était du code mort : `matches_s6_profile` redéfinissait ses
  propres cibles. Source de vérité unique rétablie.
- [audit v2] `ranking_power` étiquetait les candidats « S6 »/« T6 » alors qu'il balaie
  d = 2, 3, 4, 6 : la sortie annonçait « S6 » pour une 2-sphère. Étiquettes dérivées de
  la dimension balayée.
- [audit v2] « Les 8 chantiers » dans README.md et CLAUDE.md alors que le tableau en
  liste 12.

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
