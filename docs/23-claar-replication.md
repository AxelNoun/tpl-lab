# 23 — Réplication Claar, second sujet (déclarée avant l'asset)

**Déclaré le 21 août 2026, avant d'ouvrir le catalogue DANDI du second NWB.**

Ce n'est pas un rattrapage de `sub-551399` (H1 réfutée des deux côtés,
docs/21). Même dandiset, **autre animal**, même règle d'éligibilité, mêmes
seuils `prereg-v1`. On ne cherche pas S⁶. On ne fusionne pas les sujets.
Un INDÉCIDABLE se publie. Un second réfuté renforce la famille ; un
compatible isolé ne sauve pas Allen.

## Règle de choix (figée ici, avant la liste)

Parmi les assets de [DANDI:000458](https://dandiarchive.org/dandiset/000458)
dont `variableMeasured` contient `Units` :

1. Exclure `sub-551399` (déjà mesuré).
2. Prendre le **plus petit** contentSize restant (même critère que docs/21 :
   les petits NWB sont de l'EEG sans spikes).
3. Une session, une aire modale, pas de fusion.

Isolement, couches, horloge, plancher 100 s, seed 42, `n_boot` : identiques
à docs/21. On ne jette pas les doublons isoflurane. L'IC dégénéré
(`UNIQUE_FRAC_MIN`) n'est pas un permis de retoucher 0,1.

## Prédiction (inchangée)

H1 conjonctive : S⁶ en veille **et** delta ID (veille − iso) > 0 avec IC95
excluant 0. Déjà fausse sur le premier sujet. Ici on demande seulement si
un autre animal du même protocole produit autre chose. Verdict possible :
réfutée / compatible / INDÉCIDABLE. Pas de troisième aire « pour voir ».

## Asset retenu (après la règle, pas avant)

Catalogue DANDI 000458 : 24 NWB. Les 6 fichiers < 2 Go n'ont pas `Units`
(docs/21, EEG). Hors `sub-551399` (11,69 Go, déjà mesuré), le plus petit
NWB restant est :

`sub-590479/sub-590479_ses-20210921_behavior+ecephys.nwb`
(~12,03 Go, asset `8acbe845-c9ce-411c-81ba-77b33de17a2e`).

Même loader, même seed 42. `variableMeasured` contient `Units` (LFP,
ElectricalSeries, Units, spike sorting). Téléchargement : asset
`8acbe845-…/download/`. Si le NWB n'a pas de groupe `units` malgré la
métadonnée, le loader refuse et on passe au suivant par taille.

