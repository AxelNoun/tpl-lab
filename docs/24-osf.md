# 24 — Dépôt OSF du plan figé

Le tag git `prereg-v1` **est** le pré-enregistrement (commit
`0a5e794477c788f174f623465177b0ffee08c880`, 20 août 2026). L'OSF n'ajoute
pas un second plan : il archive le même hash, public, avec un DOI si on
enregistre le projet.

Les fichiers sont lus **dans git à ce commit**, pas dans le working tree
(`PREREGISTRATION.md` a ensuite reçu des notes IBL/Claar).

## Sans jeton (déjà public)

- GitHub : https://github.com/AxelNoun/tpl-lab/tree/0a5e794477c788f174f623465177b0ffee08c880
- Tag : `prereg-v1`
- Manifeste local :

```bash
python -m tpl.io.osf_deposit --manifest
python -m tpl.io.osf_deposit --bundle osf/prereg-v1-bundle
```

`osf/prereg-v1-bundle/` n'est pas commité (copie générée).

## Avec jeton (l'étape qui reste à l'humain)

1. Compte sur https://osf.io
2. Jeton `osf.full_write` : https://osf.io/settings/tokens
3. Puis :

```powershell
$env:OSF_TOKEN = "…"
python -m tpl.io.osf_deposit --upload
```

Ça crée un projet **public**, y dépose les 4 fichiers figés + `manifest.json`,
et imprime l'URL. Ensuite, sur OSF : *Register* → gabarit « Open-Ended
Registration » → coller le commit `0a5e794` et l'URL GitHub. L'enregistrement
OSF est irréversible ; ne pas l'improviser.

Sans jeton le script s'arrête avec le code 2. Ce n'est pas un permis de
modifier le plan.
