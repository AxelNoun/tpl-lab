# Tests supplémentaires — mêmes session et bloc, autres aires visuelles

**Déclaré le 20 août 2026, avant d'ouvrir les verdicts ci-dessous.**
Seuils inchangés (`prereg-v1`). H1-spontané est déjà réfuté sur VISp
(`docs/14-h1-spontane.md`) : cette batterie **ne peut pas** le rétablir.

## Famille (exhaustive, une ligne par aire)

Même NWB `767871931`, même plus long bloc `spontaneous` continu (1802,5 s,
jamais la somme), même pipeline `run_id` / `configs/prereg_v1.json` / seed 42.
Isolation : `quality == good` seulement.

| # | Aire | Rôle |
|---|---|---|
| 0 | VISp | test déclaré (déjà réfuté) |
| 1 | VISal | supplémentaire |
| 2 | VISam | supplémentaire |
| 3 | VISpm | supplémentaire |
| 4 | VISrl | supplémentaire |
| 5 | VISli | présente dans cette session (le prereg listait VISl, absente ici) |

VISl n'est pas dans cet enregistrement ; on ne la remplace pas par une autre
structure. On n'ajoute pas CA1, thalamus, etc. : H1-spontané était une aire
*visuelle*.

## Prédiction et lecture

Prédiction : aucune de ces cinq aires ne nomme S⁶ sous `MAX_FIT_SCORE = 3.0`
avec une ID dans une fenêtre d=6 ou d=8. Un « compatible » isolé serait
exploratoire et ne sauve pas H1. Tous les verdicts sont publiés, y compris
INDÉCIDABLE.

## Nul sur VISp (H0 du prereg, pas une nouvelle hypothèse)

Sur le même tableau VISp déjà extrait : un surrogate `phase_randomize(...,
preserve_cross=True)`, puis `run_id`. Attendu : pas S⁶ non plus (le nuage
réel n'a déjà aucun candidat). Ça ne « confirme » pas TPL ; ça vérifie que
la règle refuse aussi le nul construit sur les mêmes spectres.

## Verdicts (tous publiés)

Même bloc 4398–6200,5 s. Seed 42. Aucune aire ne nomme S⁶.

| Aire | N unités | lag | n | ID | géométrie (score) | H1 |
|---|---|---|---|---|---|---|
| VISp (déclaré) | 201 | 5 | 7210 | 37,07 | aucune (R6 41,68) | réfutée |
| VISal | 115 | 6 | 6009 | 26,87 | aucune (T6 29,92) | réfutée |
| VISam | 82 | 7 | 5150 | 24,42 | aucune (T6 28,01) | réfutée |
| VISpm | 119 | 1 | 36050 | 32,77 | aucune (T6 35,35) | réfutée |
| VISrl | 88 | 6 | 6009 | 26,54 | aucune (T6 29,61) | réfutée |
| VISli | 110 | 5 | 7210 | 26,82 | aucune (T6 28,70) | réfutée |
| nul phase VISp | 201 | 5 | 7210 | 42,85 | aucune (R6 63,32) | réfutée |

Le surrogate (`preserve_cross=True`) reste dans le même régime que le réel
(ID ~ 40, score ≫ 3). La règle refuse les deux. Ça n'autorise pas à dire
« le réel *est* un couplage linéaire » : seulement qu'il n'est pas S⁶, et
que le nul de spectre non plus.

H1-spontané n'est pas restauré. D'autres sessions restent des tests
supplémentaires, à déclarer avant.
