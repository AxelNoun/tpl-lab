# 24 — Dépôt OSF du plan figé

Le tag git `prereg-v1` **est** le pré-enregistrement (commit
`0a5e794477c788f174f623465177b0ffee08c880`, 20 août 2026). L'OSF n'ajoute
pas un second plan : il archive le même hash, public, avec un DOI si on
enregistre le projet.

Les fichiers sont lus **dans git à ce commit**, pas dans le working tree
(`PREREGISTRATION.md` a ensuite reçu des notes IBL/Claar).

## Dépôt (27 août 2026)

Projet public : **https://osf.io/fgvpz/**

Même hash que le tag `prereg-v1` (`0a5e794`). Ce n'est **pas** encore un
*Registration* OSF (pas de DOI tant qu'on n'a pas cliqué *Register* —
irréversible). GitHub reste la copie canonique du git.

## Sans jeton (déjà public)

- GitHub : https://github.com/AxelNoun/tpl-lab/tree/0a5e794477c788f174f623465177b0ffee08c880
- Tag : `prereg-v1`
- Manifeste local :

```bash
python -m tpl.io.osf_deposit --manifest
python -m tpl.io.osf_deposit --bundle osf/prereg-v1-bundle
```

`osf/prereg-v1-bundle/` n'est pas commité (copie générée).

## Enregistrement DOI (irréversible)

Le dépôt fichiers est fait. Pour un DOI : sur https://osf.io/fgvpz/,
*Register* → « Open-Ended Registration » → coller le commit `0a5e794`
et l'URL GitHub. L'enregistrement est irréversible.

Un nouveau jeton n'est utile que pour d'autres écritures API. Révoquer
tout jeton collé dans un chat ou une ligne de commande
(https://osf.io/settings/tokens). Sans jeton, `--upload` s'arrête avec
le code 2. Ce n'est pas un permis de modifier le plan.
