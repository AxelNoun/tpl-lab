# Chantier 11 — Contraste d'états et benchmark PCI (amélioration 3)

Mesure principale sur données réelles : un CONTRASTE, pas un absolu. TPL prédit
l'effondrement de la structure géométrique quand la conscience s'effondre
(veille → propofol / sommeil profond / NREM).

- Outil : `tpl.analysis.state_contrast.contrast(pts_veille, pts_anesthesie)` —
  métriques par condition (ID, b1, géométrie gagnante, score S6) + delta ID
  bootstrappé avec CI95.
- Benchmark à battre : le PCI (Casali et al. 2013, *Science Translational
  Medicine*), étalon actuel du niveau de conscience (nécessite TMS-EEG — sur les
  jeux où PCI est disponible, corréler notre « distance à la géométrie »).
- Valeur en cas d'échec de TPL : si « distance à S⁶ » suit les états de conscience
  aussi bien que le PCI, c'est un résultat publiable indépendamment de la théorie.
- Lucidité : « perception soutenue » ≠ conscience. La revendication forte exigera
  des paradigmes no-report (à documenter au moment du protocole réel).
