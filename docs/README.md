# Documentation (français)

Le README racine est la vitrine publique (anglais). Ici, le dossier scientifique
du labo, dans l’ordre utile.

## Par où commencer

1. [`../CLAUDE.md`](../CLAUDE.md) — règles non négociables.
2. [`../PREREGISTRATION.md`](../PREREGISTRATION.md) — règle de décision **figée** (`prereg-v1`).
3. [`ETAT.md`](ETAT.md) — tableau des 12 chantiers.
4. [`RESULTATS_NEGATIFS.md`](RESULTATS_NEGATIFS.md) — journal (audit + empirique).

## Concepts et protocole

| Fichier | Sujet |
|---|---|
| [01-hypothese.md](01-hypothese.md) | Ce qui reste testable après amputation de la TOE |
| [02-loi-pont.md](02-loi-pont.md) | Un point = vecteur de comptage, pas un point de S⁶ ⊂ R⁷ |
| [03-critique-tests-originaux.md](03-critique-tests-originaux.md) | Fermeture en triplets : tautologie / non-discriminante |
| [05-protocole-non-associativite.md](05-protocole-non-associativite.md) | Exige un labo (TMS / optogénétique) |
| [08-psychophysique.md](08-psychophysique.md) | Protocole seul |
| [09-geometries-candidates.md](09-geometries-candidates.md) | S⁶ vs T⁶ vs R⁶ ; cutoff 3,0 |
| [22-mgplvm.md](22-mgplvm.md) | GP géodésique (stand-in mGPLVM) ; secondaire ; T⁶ non récupéré |
| [10-multiplets-spectraux.md](10-multiplets-spectraux.md) | Spectre à 4 niveaux, pas un « plateau de 27 » |
| [11-contraste-etats.md](11-contraste-etats.md) | Outil PCI-like ; pas de jeu spike Allen |
| [12-calibration.md](12-calibration.md) | Puissance, TPR, bruit, IC |
| [13-donnees-reelles.md](13-donnees-reelles.md) | Loader, durée, interdiction de concaténer |

## Tests empiriques (Allen)

| Fichier | Quoi |
|---|---|
| [14-h1-spontane.md](14-h1-spontane.md) | Premier test déclaré — VISp, session 767871931, **réfuté** |
| [15-aires-supplementaires.md](15-aires-supplementaires.md) | Même bloc, autres aires VIS — 6/6, famille écrite avant |
| [16-replication-session.md](16-replication-session.md) | Autre souris 766640955 — 6/6, déclarée avant le NWB |
| [17-ibl.md](17-ibl.md) | IBL — autre jeu, déclaré avant les spikes ; pas un rattrapage Allen |
| [18-ibl-visp.md](18-ibl-visp.md) | Première insertion VISp IBL, spontané 10 min — **INDÉCIDABLE** |
| [19-ibl-session.md](19-ibl-session.md) | Même insertion, session continue 97 min — encore **INDÉCIDABLE** |
| [20-nul-lowrank.md](20-nul-lowrank.md) | Nul RNN rang faible structuré (synth_) — réfuté, n = 8236 |
| [21-claar-contraste.md](21-claar-contraste.md) | DANDI 000458, PL, veille/isoflurane — H1 réfutée des deux côtés |
| [23-claar-replication.md](23-claar-replication.md) | Second sujet Claar, déclaré avant l'asset (`sub-590479`) |

Onboarding : [onboarding/PARCOURS.md](onboarding/PARCOURS.md),
[onboarding/RESSOURCES.md](onboarding/RESSOURCES.md).
