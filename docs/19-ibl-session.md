# IBL session continue — même insertion, autre famille

**Déclaré le 21 août 2026, après l'INDÉCIDABLE du spontané (`docs/18`),
avant cet extract.** Seuils inchangés (`prereg-v1`).

Le spontané IBL (~10 min) ne peut pas atteindre n_min après décimation.
Les alternatives écartées :

- coller RFM / replay / essais : concaténation, interdite ;
- une autre insertion choisie après l'INDÉCIDABLE : HARKing ;
- le protocole passif entier (~20 min) : encore sous l'avertissement 45 min.

**Famille retenue :** la même insertion déjà choisie par `docs/17`
(eid `5ae68c54-2897-4d3a-8120-426150704385`, pid
`a8a59fc3-a658-4db4-b5e8-09f1e4df03fd`, VISp, label = 1). Intervalle =
horloge continue `[min(spikes.times), max(spikes.times)]` du tri
`pykilosort/#2024-05-06#`. Ce n'est **pas** du spontané : la tâche IBL est
dedans. Ce n'est pas une concaténation : un seul intervalle d'horloge.

Prédiction : `select_geometry` ne nomme pas S⁶. Un compatible ici n'est pas
Allen restauré, ni un percept contrôlé. Un INDÉCIDABLE reste un INDÉCIDABLE.

## Extract (après la déclaration ci-dessus)

Horloge : 0,001 → 5852,455 s (**97,5 min**). 17 good VISp6a. 117049 fenêtres
de 50 ms. Pas de PCA, pas de z-score, pas de collage d'essais.

```
117049 fenêtres -> décimation 1/1000 -> 118 échantillons
INDECIDABLE : autocorrelation jamais descendue sous 0.1 en 1000 pas
```

La série n'est pas décorrélable sous le seuil figé 0,1. Ce n'est pas un
permis de le desserrer, ni de changer la fenêtre 50 ms. Même cause plus
sévère que le spontané de 10 min (là, lag 9 et n = 1334 ; ici le lag tape
le plafond 1000).

Allen 12/12 n'est pas restauré. IBL, sur cette insertion, n'a pas de
verdict géométrique sous `prereg-v1`.

