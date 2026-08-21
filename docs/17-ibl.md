# IBL Brain-wide Map — autre jeu, déclaré avant les spikes

**Déclaré le 21 août 2026, avant tout téléchargement IBL.**
Seuils inchangés (`prereg-v1`). H1-spontané Allen est déjà réfuté 12/12
(docs/14–16) : un résultat IBL **ne peut pas** le rétablir.

## Ce que ce n'est pas

Ce n'est pas H1 perceptif, ni H1-spontané Allen. L'IBL est une tâche de
décision (stimulus brefs, essais). Concaténer les essais ou les ITI est
**interdit** (même règle que les gratings Allen, `tpl.io.extract`).

Le protocole passif IBL a trois morceaux : activité spontanée (écran gris),
carte réceptive, replay de la tâche. Seul le premier est un analogue du bloc
`spontaneous` Allen. RFM et replay ne sont pas fusionnés avec lui.

## Famille du premier test IBL

- Intervalle : `spontaneousActivity` de `passivePeriods` — **un** intervalle
  continu, jamais la somme avec RFM / replay / essais.
- Si cet intervalle dure < 100 s : le loader refuse. INDÉCIDABLE n'est pas une
  raison de concaténer.
- Isolation : label IBL publié `clusters.label == 1` (« good »), rien d'autre
  (pas de coupure taux / sliding RP).
- Aire : un acronyme CCF, couches d'une même aire regroupées (`VISp` + `VISp5`
  + `VISp6a`). `VISp` ne ramasse pas `VISpm`.
- Pipeline : `run_id` / `configs/prereg_v1.json` / seed 42.
- Insertion : la première insertion Brain-wide Map en cortex visuel (`VIS*`)
  qui a un bloc spontané ≥ 100 s **et** N ≥ 7 good units dans une aire VIS —
  choisie sur métadonnées, pas en cherchant S⁶.

## Prédiction et lecture

Prédiction : `select_geometry` ne nomme pas S⁶. Un « compatible » isolé est
exploratoire et ne sauve pas Allen. Tous les verdicts sont publiés, y compris
refus du loader et INDÉCIDABLE.
