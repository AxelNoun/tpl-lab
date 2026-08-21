# Réplication — autre session Allen, même règle

**Déclaré le 21 août 2026, avant téléchargement du NWB.**
Seuils inchangés (`prereg-v1`). H1-spontané est déjà réfuté sur la session
`767871931` (docs/14, docs/15) : cette réplication **ne peut pas** le rétablir.

## Choix de la session (métadonnées seulement)

Première ligne `session_type == functional_connectivity` de `sessions.csv`
qui n'est pas `767871931` : **766640955** (specimen 744912849, mâle, wt/wt,
133 jours). Autre animal que 767871931 (specimen 753795610). Même type de
protocole (blocs spontaneous longs). Pas de regard sur les spikes, les
aires, ni la durée avant ce paragraphe.

## Famille

- Plus long bloc `spontaneous` continu (jamais la somme).
- Toutes les structures dont l'acronyme commence par `VIS`, `quality == good`,
  N ≥ 7. Pas CA1, pas thalamus, pas fusion.
- `run_id` / `configs/prereg_v1.json` / seed 42.
- Toutes les aires présentes sont publiées, y compris INDÉCIDABLE.

## Prédiction et lecture

Prédiction : aucune aire ne nomme S⁶. Un « compatible » isolé est exploratoire
et ne sauve pas H1. Si le plus long spontané est < 100 s, le loader refuse et
c'est un écart de protocole, pas une raison de concaténer.

## Verdicts (tous publiés)

Bloc spontané 4398–6200,5 s (1802,5 s), 6 blocs présents, somme non utilisée.
Seed 42. **6/6 réfutées.**

| Aire | N | lag | n | ID | géométrie (score) | H1 |
|---|---|---|---|---|---|---|
| VISp | 119 | 2 | 18025 | 23,61 | aucune (S6 26,75) | réfutée |
| VISal | 173 | 4 | 9013 | 28,73 | aucune (R6 32,42) | réfutée |
| VISam | 126 | 4 | 9013 | 29,24 | aucune (T6 32,59) | réfutée |
| VISl | 98 | 4 | 9013 | 20,97 | aucune (R6 24,55) | réfutée |
| VISrl | 80 | 6 | 6009 | 21,77 | aucune (S6 25,50) | réfutée |
| VISmma | 127 | 1 | 36050 | 29,85 | aucune (T6 32,36) | réfutée |

Deux aires (VISp, VISrl) ont **S⁶ en tête du ranking** avec un score ~25–27,
dix fois le seuil 3,0 : `rank_candidates` seul aurait menti ; `select_geometry`
refuse. H1 n'est pas restauré.

Deux souris, 12 paires (session × aire visuelle), 12 réfutations. Une 13ᵉ
paire serait toujours un test supplémentaire.
