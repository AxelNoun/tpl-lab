# H1-spontané — premier test empirique (session Allen 767871931)

**Date : 20 août 2026.** Seuils inchangés (tag `prereg-v1` = `0a5e794`).
Ce n'est pas H1 perceptif. C'est le test plus faible déclaré dans
`PREREGISTRATION.md` : un bloc `spontaneous` continu, une aire, éveillé.

## Commandes

```bash
# NWB 2,64 Go, non commité (data/ est gitignoré)
# session functional_connectivity 767871931, fichier Allen
# well_known_file 1026124194
curl.exe -L -o data/allen/session_767871931/session_767871931.nwb \
  "http://api.brain-map.org/api/v2/well_known_file_download/1026124194"

# allensdk exige Python 3.11 ; le cœur du labo tourne en 3.14.
# Le NWB 2019 n'est pas lu par pynwb/hdmf récents (NWBFile.external_resources).
# --nwb passe par h5py (tpl.io.allen.read_ecephys_nwb).
python -m tpl.io.allen --nwb data/allen/session_767871931/session_767871931.nwb --list
python -m tpl.io.allen --nwb data/allen/session_767871931/session_767871931.nwb \
    --area VISp --stimulus spontaneous --out data/real_VISp.npy
python -m tpl.analysis.run_id --config configs/prereg_v1.json \
    --data data/real_VISp.npy --seed 42
```

## Ce qui a été pris (et refusé)

- Une aire : **VISp**, 201 unités `quality == good`. Pas de fusion d'aires,
  pas de coupure sur le taux / SNR / ISI.
- Un seul bloc : le plus long `spontaneous` = **1802,5 s** (6 blocs existent ;
  la somme 2335 s n'a pas été utilisée).
- Gratings, gabors, flashes, movies : max ≤ 2 s, refusés par le plancher 100 s.
- Pas de PCA vers 7, pas de z-score.

Le bloc dure 30 min < 45 min : `extract_block` a averti. Après décimation,
n = 7210 ≥ 2000 → **décidable**, pas INDÉCIDABLE.

## Verdict (règle figée)

```
36050 fenêtres -> décimation 1/5 -> 7210 échantillons indépendants
mesure 1 : ID = 37.07 >= 8.5  -> réfutée
mesure 2 : AUCUNE (meilleur R6, score 41.68 > 3.0)  -> réfutée
verdict H1 (les deux) : RÉFUTÉE
```

TwoNN a jeté 3 doublons exacts sur 7210 (avertissement déjà prévu) : négligeable.

## Lecture autorisée

H1-spontané, sur **cette** aire de **cette** session, n'est pas compatible avec
S⁶. La preregistration disait déjà : un réfutant ici réfute aussi H1 perceptif
(si la variété n'apparaît même pas sans stimulus contrôlé, la revendication plus
forte tombe).

Ce n'est pas une preuve que « le cortex n'a pas de variété » en général, ni
un permis d'aller chercher une autre aire jusqu'à obtenir S⁶ (HARKing).
D'autres aires / sessions sont des tests *supplémentaires*, avec une
multiplicité à déclarer avant de les lancer.

L'autocorrélation biaise TwoNN **vers le bas**. Un lag 5 trop petit aurait
sous-estimé l'ID, pas produit 37. Le réfutant « trop haut » n'est donc pas un
artefact de sous-décimation.

## Ce que ce n'est pas

- Pas un contraste d'états (Allen Visual Coding est éveillé seulement).
- Pas un percept contrôlé.
- Pas une confirmation d'un nul : on n'avait pas besoin d'un nul pour
  *réfuter* une prédiction manquée. Un nuage 201-D qui n'est ni S⁶ ni T⁶ ni R⁶
  est exactement ce que la règle conjonctive nommée doit refuser.
