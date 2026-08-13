# Pourquoi les tests proposés par l'article source ne testent rien d'octonionique

## 1. Fermeture de phase en triplets
Si θ_ab := θ_a − θ_b (différences de phases), alors
θ_ab + θ_bc + θ_ca = (θ_a−θ_b)+(θ_b−θ_c)+(θ_c−θ_a) ≡ 0. Identiquement. Pour tout
système. La « signature » est une tautologie algébrique.

Si au contraire chaque θ_xy est estimé indépendamment (Hilbert par paire, bruit),
la somme n'est plus exactement 0 — mais elle est proche de 0 pour n'importe quel
système d'oscillateurs couplés. Démonstration : `python -m tpl.demo` la calcule sur
un Kuramoto standard. Un test que le nul réussit n'est pas un test.

## 2. Phases et non-associativité
Les phases vivent dans U(1)^n : groupe abélien, donc associatif. Aucune statistique
de phases ne peut détecter un défaut d'associativité. Pour tester l'associateur,
il faut composer des OPÉRATIONS dans un ordre contrôlé → interventionnel (chantier 5).

## 3. « Symétrie d'ordre 3 » et SU(3)
SU(3) est un groupe de Lie continu à 8 paramètres. Le « 3 » est la dimension de la
représentation fondamentale, pas une rotation discrète de 120°. Chercher des motifs
ternaires dans un espace d'états ne teste pas SU(3).

## 4. Boucles persistantes (TDA)
L'homologie persistante de signaux fMRI produit couramment des H1 durables dans des
modèles nuls (dynamiques oscillantes génériques). Sans comparaison aux nuls ET sans
prédiction quantitative (combien de boucles, quelle persistance), ce n'est pas
discriminant.

Conclusion : la seule prédiction rigide extractible est la dimension intrinsèque
(6 ou 8). C'est le chantier 6.
