# Chantier 5 — Protocole (futur) : tester la non-associativité

**Statut : expérience à faire. Intestable sur données passives, par principe.**

Idée : si une multiplication octonionique effective existe, la composition de trois
perturbations doit dépendre du parenthésage : (A∘B)∘C ≠ A∘(B∘C), associateur ≠ 0.

Esquisse :
- 3 sites corticaux (TMS multi-site ou optogénétique 3 cibles chez l'animal).
- Conditions : [(A puis B, fenêtre courte) puis C] vs [A puis (B puis C)] avec délais
  contrôlés pour manipuler le groupement temporel, ordre total identique.
- Mesure : divergence des trajectoires de population post-perturbation (distance
  d'états, pas seulement amplitude évoquée).
- Nuls : modèles linéaires (associatifs par construction) ajustés aux mêmes réponses
  simples ; toute non-linéarité générique doit aussi être écartée — c'est LA difficulté :
  distinguer « non-associatif au sens algébrique » de « non-linéaire banal ».

Prérequis : chantier 2. A, B et C composent des déplacements du vecteur de
population dans R^N (la ligne 1 de la loi-pont), pas des éléments d'une base
d'octonions — cette identification n'a pas de procédure et n'est donc pas une
prédiction. Le protocole dit *quoi* on compose ; distinguer « non-associatif au
sens algébrique » de « non-linéaire banal » reste LA difficulté, et sans elle
l'expérience reste une métaphore de l'octonion, pas un test.
