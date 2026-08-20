# Chantier 11 — Contraste d'états et benchmark PCI (amélioration 3)

Mesure principale sur données réelles : un CONTRASTE, pas un absolu. TPL prédit
l'effondrement de la structure géométrique quand la conscience s'effondre
(veille → propofol / sommeil profond / NREM).

- Outil : `tpl.analysis.state_contrast.contrast(pts_veille, pts_anesthesie)` —
  métriques par condition (ID, b1, géométrie gagnante, score S6) + delta ID et son
  intervalle. L'intervalle vient d'un SOUS-ÉCHANTILLONNAGE SANS REMISE (m parmi n) :
  le bootstrap avec remise est invalide pour un estimateur k-NN, les duplicats
  gonflaient l'ID de 5,95 à 9,02 (audit v2, docs/RESULTATS_NEGATIFS.md). Calculé à
  m < n, il est conservateur et n'est pas recentré ; n_boot ≥ 1000.

## Ce que l'intervalle vaut, et ce qu'il ne vaut pas

Mesuré par `python -m tpl.analysis.calibration --ci-coverage`, qui compare
l'intervalle à une vraie différence connue par construction (n = 1200) :

| contraste | vraie différence | couverture (naïf) | couverture (rescalé √(m/n)) |
|---|---|---|---|
| S⁶ vs S³ | 3 | 98 % | 65 % |
| S¹⁰ vs S³ | 7 | 40 % | 32 % |

Deux enseignements, tous deux négatifs.

**La correction de manuel dégrade l'intervalle.** Rescaler la racine θ_m − θ_n par
√(m/n) (Politis & Romano 1994) est le correctif principiel d'un intervalle calculé
à m < n. Il fait chuter la couverture. Raison : le biais de TwoNN bouge à peine
entre m = 0,632 n et n, donc le sous-échantillonnage ne peut pas le détecter. La
largeur excédentaire du calcul à m < n (facteur ≈ 1,26) était la seule chose qui
compensait ce biais ; la retirer laisse le biais nu. Les 98 % du cas 6 contre 3
sont donc une compensation de deux erreurs, pas une propriété.

**En dimension élevée, rien ne sauve l'intervalle.** À 10 contre 3, le biais sur la
différence (≈ 1,3) dépasse la largeur de l'intervalle (≈ 1,5) : aucun schéma de
rééchantillonnage ne peut le réparer, puisqu'aucun n'a accès au biais. Ce qui
survit est le signe : le biais croît avec d, donc la différence est SOUS-estimée et
l'intervalle tiré vers zéro. Le critère « IC95 exclut 0 » reste conservateur, mais
la largeur ne doit jamais être publiée comme barre d'erreur.
- Benchmark à battre : le PCI (Casali et al. 2013, *Science Translational
  Medicine*), étalon actuel du niveau de conscience (nécessite TMS-EEG — sur les
  jeux où PCI est disponible, corréler notre « distance à la géométrie »).
- Valeur en cas d'échec de TPL : si « distance à S⁶ » suit les états de conscience
  aussi bien que le PCI, c'est un résultat publiable indépendamment de la théorie.
- Lucidité : « perception soutenue » ≠ conscience. La revendication forte exigera
  des paradigmes no-report (à documenter au moment du protocole réel).
