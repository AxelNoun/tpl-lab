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
