# Nul RNN à rang faible structuré (Mastrogiuseppe & Ostojic)

**Date : 21 août 2026.** Seuils inchangés (`prereg-v1`). Données `synth_` uniquement.

U,V indépendants et `UUᵀ` avaient été mesurés et écartés (pas de dynamique
collective / points fixes → boule de bruit 200-D). Il restait le recouvrement
structuré de Mastrogiuseppe & Ostojic (2018) : `W = (g/N) m nᵀ` avec une
géométrie imposée entre les colonnes de `m` et de `n`.

Construction retenue (`tpl.nulls.rnn.simulate_lowrank_rnn`, mode
`oscillatory`) : paires `(m_i, m_j)` avec
`n_i = (ρ/√2)(m_i + m_j)`, `n_j = (ρ/√2)(-m_i + m_j)`. La circulation pure
(`n_i = ρ m_j`, `n_j = -ρ m_i`) a des valeurs propres `-1 ± i gρ` et meurt
à l'origine ; le morceau aligné permet une bifurcation de Hopf.

## Mesure (seed 42, `synth_lowrank_r6.npy`)

200 unités, rang 6, ρ = 0,8, `g_struct` = 4, 140 000 pas. Pipeline figé.

```
140000 fenêtres -> décimation 1/17 -> 8236 échantillons
mesure 1 : ID = 14.95 >= 8.5  -> réfutée
mesure 2 : AUCUNE (meilleur R6, score 36.76 > 3.0)  -> réfutée
verdict H1 : RÉFUTÉE
```

Le nul est maintenant un adversaire réel (série décorrélable, n ≥ 2000). Il
perd sur les deux mesures. Rang 6 dans W n'est pas une variété S⁶ dans l'espace
des unités, et `g` / ρ ne sont pas réglés vers d = 6.

Ce n'est pas une donnée empirique.
