# Chantier 6/11 — Données réelles (loader)

Rien n'est téléchargé ni commité ici. Le loader produit un `.npy`
`(n_fenêtres, n_unités)` que `run_id` consomme. Il ne réduit pas à R⁷.

```bash
pip install -e ".[full]"   # allensdk, optionnel ; Python 3.11 (pas 3.14)
# ou, NWB déjà sur disque (évite pynwb) :
python -m tpl.io.allen --nwb data/allen/session_767871931/session_767871931.nwb --list
python -m tpl.io.allen --nwb data/allen/session_767871931/session_767871931.nwb \
    --session 767871931 --area VISp --stimulus spontaneous --out data/real_VISp.npy
python -m tpl.analysis.run_id --config configs/prereg_v1.json --data data/real_VISp.npy
```

## Constat de puissance (figé avant tout contact avec des données)

H1 tel qu'écrit (« percept constant > 10 s ») n'est **pas puissant** sur du
Neuropixels public à stimuli brefs.

| durée brute | fenêtres 50 ms | puissant à lag 1 | puissant à lag 10 | puissant à lag 25 |
|---|---|---|---|---|
| grating Allen (~2 s) | 40 | non | non | non |
| percept « > 10 s » | 200 | non | non | non |
| plancher lag 1 | 100 s | oui (tout juste) | non | non |
| spontané ~20 min | 24 000 | oui | oui | non (il faut 42 min) |
| budget prereg (lag 25–55) | 45–90 min | oui | oui | oui |

100 repeats d'un grating de 2 s *sommés* feraient 200 s et passeraient le plancher
à lag 1. Le loader **interdit la concaténation** : la durée qui compte est celle du
plus long bloc continu, pas la somme des essais. C'est une hypothèse différente
(variété stationnaire *entre* essais, pas trajectoire d'un percept soutenu) et elle
n'est pas dans H1.

`extract_block` refuse tout intervalle < 100 s. En dessous de 45 min il avertit :
`run_id` pourra renvoyer INDÉCIDABLE après décimation, et ce n'est pas une raison
de baisser n_min.

## Ce qui EST testable sur Allen Visual Coding

Allen Visual Coding Neuropixels est **éveillé uniquement** (pas d'anesthésie → pas
de contraste d'états sur ce jeu). Le seul bloc assez long est en général
`spontaneous`. Ce n'est pas un percept contrôlé. La revendication testable, déclarée
comme telle :

> la dynamique de population d'une aire visuelle, éveillée, sans stimulus
> contrôlé, sur un bloc continu assez long, a-t-elle une géométrie S⁶ ?

C'est strictement plus faible que « géométrie d'un percept soutenu ». Ce n'est
pas un substitut silencieux.

Aires, une à la fois (jamais fusionnées) : VISp, VISl, VISal, VISpm, VISam, VISrl.
Filtre d'isolation : le label `quality == 'good'` du SDK, rien d'autre (pas de
coupure sur le taux, le SNR ou les violations ISI).

Premier test déclaré (docs/14) : session `767871931`, VISp, bloc spontané 1803 s.
Verdict **réfuté** (ID = 37, pas de géométrie sous 3,0). D'autres aires ne se
lancent pas « jusqu'à trouver S⁶ ».

## Contraste veille / anesthésie

Pas de source publique Neuropixels *spike* avec les deux états dans ce dépôt.
L'EEG OpenNeuro serait un autre observable (pas des comptages de spikes) et
exigerait une nouvelle ligne de loi-pont. En attendant, le chantier 11 reste
un outil sans données.
