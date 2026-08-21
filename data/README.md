# Data

Nothing in this folder is committed except this README. Simulated files must
use the `synth_` prefix. Real extracts use names like `real_VISp.npy` and
must not be prefixed `synth_`.

## Allen Visual Coding Neuropixels (awake only)

Public NWB files, not stored in git.

| Session | Specimen | Well-known file | Role |
|---|---|---|---|
| 767871931 | 753795610 | 1026124194 | Declared first test + extra visual areas |
| 766640955 | 744912849 | 1026124293 | Replication (declared before download) |

```bash
pip install -e ".[nwb]"
python -m tpl.io.allen --nwb data/allen/session_SESSION/session_SESSION.nwb --list
python -m tpl.io.allen --nwb data/allen/session_SESSION/session_SESSION.nwb \
    --area VISp --stimulus spontaneous --out data/real_VISp.npy
python -m tpl.analysis.run_id --config configs/prereg_v1.json --data data/real_VISp.npy
```

Download URLs: `http://api.brain-map.org/api/v2/well_known_file_download/FILE_ID`

See `docs/13-donnees-reelles.md` and `docs/14-h1-spontane.md`. Do not concatenate
short trials. Isolation filter: `quality == good` only.

## Not yet in this repo

- IBL Brain-wide Map — loader `python -m tpl.io.ibl` (docs/17). First declared
  extract: eid `5ae68c54-2897-4d3a-8120-426150704385`, VISp, 600.1 s
  spontaneous → `data/real_ibl_VISp.npy` (INDECIDABLE). Same insertion, full
  clock 97.5 min → `data/real_ibl_VISp_session.npy` (still INDECIDABLE;
  autocorr never < 0.1 in 1000 lags). See `docs/18` and `docs/19`.
- Wake / anesthesia spike contrast — no public set wired; OpenNeuro EEG would
  need a new bridge law (`docs/02-loi-pont.md`).
