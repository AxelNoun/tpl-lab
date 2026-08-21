# Contraste veille / isoflurane — DANDI 000458 (Claar et al.)

**Déclaré le 21 août 2026, avant le téléchargement du NWB.**
Seuils inchangés (`prereg-v1`). Allen n'a pas d'anesthésie ; IBL n'en a pas.
Ce n'est **pas** un rattrapage de H1-spontané (12/12 réfuté) ni d'IBL
(INDÉCIDABLE).

Jeu : [DANDI:000458](https://dandiarchive.org/dandiset/000458)
(Claar, Rembado et al. 2023). Neuropixels + isoflurane, **même animal**,
époques veille puis anesthésie. Les NWB < 2 Go de ce dandiset sont de l'EEG
sans `units` ; seuls les assets listant `Units` sont éligibles.

## Famille du premier contraste

- Session : plus petit asset dont les métadonnées DANDI listent `Units`
  (les NWB < 2 Go de ce dandiset sont de l'EEG sans spikes ; les utiliser
  casserait la loi-pont). Chemin :
  `sub-551399/sub-551399_ses-20210128_behavior+ecephys.nwb` (~11,7 Go).
- Isolation : unités déjà fournies (QC des auteurs). Si une colonne `quality`
  existe, `good` seulement — pas de coupure taux / SNR.
- Aire : un acronyme CCF, couches pliées comme IBL (`VISp` + `VISp5`). Modal
  parmi les good units ; N ≥ 7. Pas de fusion d'aires.
- Temps : le plus long intervalle continu **veille** et le plus long
  **isoflurane / maintained** dans `intervals/`. Un intervalle d'horloge par
  état, pas une concaténation d'essais de stim. La stim corticale du protocole
  Claar **fait partie** de l'époque : ce n'est pas du spontané, ni du PCI
  (TMS-EEG).
- Si un état dure < 100 s : le loader refuse. INDÉCIDABLE n'est pas une
  raison de coller les essais ni de desserrer l'autocorr 0,1.
- Pipeline : `extract_block` + `run_id --data A --data-b B --seed 42`.

## Prédiction (prereg, non retouchée)

TPL : delta ID (veille − isoflurane) > 0, IC95 exclut 0 ; sous isoflurane
`best_geometry` ≠ S⁶ (y compris None). Un compatible isolé ne sauve pas Allen.
Un INDÉCIDABLE se publie.

## Extract (après la déclaration)

Session `sub-551399_ses-20210128` (DANDI asset `942c7978-…`). Aire modale
**PL** (205 unités, QC des auteurs, pas de colonne `quality`). Veille = horloge
avant l'induction (0 → 1787 s). Isoflurane = époque `isoflurane_anesthesia`
(1659 s). Induction (273 s) non collée.

```
veille :      35739 fenêtres -> 1/6 -> 5957
              ID = 39.20  géométrie AUCUNE (T6, 43.89)  -> RÉFUTÉE
isoflurane :  33188 fenêtres -> 1/1 -> 33188
              ID = 29.64  géométrie AUCUNE (S6, score nan)  -> RÉFUTÉE
```

Sous isoflurane, TwoNN jette 30677 / 33188 doublons exacts (~92 %) : le nuage
de comptages à 50 ms est presque un point. Le score nan du fingerprint vient
d'une médiane de distances nulle. Ce n'est pas S⁶. Ce n'est pas un permis de
filtrer les zéros.

Le contraste à n_boot = 1000 du prereg n'est pas publié : 1000 TwoNN sur une
série à 92 % de doublons n'est pas un IC, c'est un goulot. Le delta ponctuel
39,20 − 29,64 n'est pas une barre d'erreur. La clause secondaire du prereg
(géométrie ≠ S⁶ sous anesthésie) est tenue ; la clause « S⁶ en veille » ne l'est
pas. Allen n'est pas restauré.

