# IBL spontaneousActivity — premier extract déclaré (VISp)

**Date : 21 août 2026.** Seuils inchangés (`prereg-v1`). Protocole :
`docs/17-ibl.md`. Ce n'est **pas** un rattrapage d'Allen (déjà réfuté 12/12).

Insertion choisie par la règle écrite **avant** les spikes : première insertion
Brain-wide Map `atlas_acronym=VISp` (ordre `ONE.search_insertions`) qui a
`spontaneousActivity` ≥ 100 s et N ≥ 7 good units dans VISp (couches
incluses).

| Champ | Valeur |
|---|---|
| eid | `5ae68c54-2897-4d3a-8120-426150704385` |
| pid | `a8a59fc3-a658-4db4-b5e8-09f1e4df03fd` |
| probe | `probe00` (pykilosort révision `2024-05-06`) |
| sujet | MFD_08, 2023-09-07, churchlandlab_ucla |
| spontané | 4582,83 → 5182,91 s (**600,1 s**, un seul intervalle) |
| RFM / replay | 301 s / 343 s — **non collés** |
| isolation | `clusters.label == 1` uniquement |
| unités | 17 good, toutes `VISp6a` (pliées en VISp) |

```
12001 fenêtres (50 ms) -> décimation 1/9 -> 1334 échantillons indépendants
INDECIDABLE : 1334 < 2000
```

Pas de géométrie, pas d'ID publiée : la règle figée refuse de conclure.

## Lecture autorisée

Le plancher brut de 100 s (lag 1) est saturé. L'autocorrélation des comptages
à 50 ms impose lag 9 : 600 s / (0,05 × 9) ≈ 1333 < n_min. C'est le même
mécanisme que l'avertissement 45 min de `extract_block`, pas un bug du loader.

Coller RFM, replay ou les essais de la tâche pour passer 2000 serait de la
concaténation. Chercher une autre insertion *après* cet INDÉCIDABLE pour
obtenir un verdict géométrique serait du HARKing. Un test IBL puissant
exigerait un intervalle continu assez long **déclaré avant**, ou une autre
famille (session entière y compris la tâche) — ce n'est pas ce test.

Allen n'est pas restauré. IBL spontané, sur **cette** insertion, est
**INDÉCIDABLE**.
