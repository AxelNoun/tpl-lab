# Ressources (références valides)

L'article Substack source de la conjecture n'est **pas** une référence. Ci-dessous
ce que le dépôt utilise réellement, tout en accès ouvert ou standard.

## Estimateurs et inférence

- Facco, d'Errico, Rodriguez, Laio (2017). *Estimating the intrinsic dimension of datasets by a minimal neighborhood information*. Scientific Reports. TwoNN (`tpl.analysis.intrinsic_dim`).
- Osada, Funkhouser, Chazelle, Dobkin (2002). *Shape distributions*. ACM TOG. Histogramme des distances du fingerprint.
- Jensen, Kao, Tripodi, Hennequin (2020). *Manifold GPLVMs for discovering non-Euclidean latent structure in neural data*. Upgrade documenté, pas encore le test primaire.
- Platt (1964). *Strong inference*. Science. Question « quelle géométrie ? » plutôt que « TPL vraie ? ».
- Politis & Romano (1994). *Large sample confidence regions based on subsamples*. La construction √(m/n) a été **mesurée et rejetée** pour TwoNN (docs/11).
- Ioannidis (2005). *Why most published research findings are false*. PLoS Medicine.

## Algèbre (faits déjà établis dans le dépôt)

- Baez (2002). *The octonions*. Bull. Amer. Math. Soc. G2 = Aut(O), G2/SU(3) ≅ S⁶.
- Table de Fano / multiplication octonionique : `tpl.utils.octonions`, tests Moufang et alternativité.

## Neuroscience (données et nuls)

- Claar, Rembado et al. (2023). Simultaneous EEG, Neuropixels, and cortical
  stimulation in head-fixed mice. DANDI:000458. Contraste veille/isoflurane
  (`docs/21`) ; ce n'est pas du PCI.
- Casali et al. (2013). *A theoretically based index of consciousness*. Sci. Transl. Med. Benchmark PCI du contraste d'états — TMS-EEG, pas notre observable.
- Gardner, Hermansen, Pachitariu et al. (2022). *Toroidal topology of population activity in grid cells*. Nature. T⁶ comme rival naturel.
- Sompolinsky, Crisanti, Sommers (1988). Chaos in random neural networks. Nul RNN.
- Mastrogiuseppe & Ostojic (2018). *Linking connectivity, dynamics and computations in low-rank RNNs*. Neuron. Rang faible à recouvrement structuré — `simulate_lowrank_rnn` ; U,V indépendants et UUᵀ restent écartés.

## Ce qui n'est pas une source

Toute reformulation « VSA-TOE / Topological Phase-Locking » publiée hors revue. Le projet la rend falsifiable ; il ne la cite pas.
