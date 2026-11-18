# Reproduction guide

Complete end-to-end reproducibility is **not** claimed. This guide states what can and cannot be reproduced.

## Levels
| Level | What | Possible from the releases? |
|---|---|---|
| 0 | Extract regional series from the source products in Google Earth Engine (`gee/`) | Needs the author's private study-area polygon (not included) and an Earth Engine account. Scripts were run by the author; **not run in QA** (syntax-checked only). |
| 1 | Phase 2C v3 detection and Phase 2D/2G outputs from the stored backbone and event tables (original notebooks in `notebooks/`) | The notebooks were re-run in a scratch environment from the stored inputs (`notebooks/README.md`). The backbone is not released, so Phase 2C cannot be started from the release alone. |
| 2 | Detection audit, statistics and Eq. 6/7 audit scripts from the derived data | **Yes** (steps below). Executed and compared with stored outputs in the release QA (`qa_results.json`, `QA_REPORT.md`). |
| 3 | Figures 2–4 from derived data | Yes (steps below). Figure 1 needs the polygon and Bangladesh outline (not included). |
| 4 | Phase 7A extended robustness analysis | Yes, with file B, the sanitised chunks and the 39-row catalogue (`documentation/PHASE7A_INPUT_PROVENANCE.md`). The stored Candidate Audit cannot be fully reproduced. |
| not possible | Phases 2A, 2E and 2F from the releases | Source extracts, the chunk-merge workflow and quality-control inputs are missing (`MISSING_INPUTS_AND_PERMISSIONS.md`). |

## Steps (Levels 2–3)
1. Download the software release and the Zenodo derived-dataset record. Unzip the dataset so that its `data/` folder sits next to `scripts/`.
```
python -m pip install -r requirements.txt        # Python >= 3.10; QA was run with Python 3.13
python scripts/stage_flat_inputs.py              # builds data/derived/ (flat view) from the topic folders
python scripts/detection/independent_detector_and_chronology_audit.py
python scripts/statistics/association_tests_reproduction.py
python scripts/statistics/consensus_event_analysis.py
python scripts/statistics/cross_response_exact_permutation.py
python scripts/statistics/seasonal_control_audit.py
python scripts/statistics/response_minimum_window_fraction.py
python scripts/eq6_eq7_audit/eq6_reconstruction_audit.py
python scripts/eq6_eq7_audit/eq6_35pentad_soilwater_offsets.py
python scripts/eq6_eq7_audit/eq7_fullrecord_checks.py              # 3,285-pentad recomputation vs stored series (zone-level inputs)
python scripts/eq6_eq7_audit/eq7_pathway_comparison.py
python scripts/eq6_eq7_audit/eq7_percentile_and_drift_tests.py   # needs the previous script's output
python scripts/eq6_eq7_audit/eq7_sm_catalogue_stress.py
python scripts/eq6_eq7_audit/eq7_driver_flag_stress.py
python scripts/eq6_eq7_audit/downstream.py                       # slow (minutes)
python scripts/figures/AEZ26_Fig2_Catalogue/make_AEZ26_Fig2.py --data-dir data/derived --out-dir out/fig2
```
Statistics outputs are written to `results/phase1_closure/` and audit outputs to `results/eq6_eq7_rerun/` (created on first run); the stored reference copies are in `data/statistical_outputs/closure_checks/` and `data/eq6_eq7_verification/` of the dataset record. The scripts are kept as originally written and read `data/derived/`, hence the staging step.
Run all checks (syntax, notebooks, JSON/CSV, JS syntax, manifest, duplicates, scans, re-execution and comparison, figure tests): `python scripts/qa/run_release_checks.py` (several minutes; needs `data/`).

The Eq. 7 recomputation from per-pixel exports (`scripts/eq6_eq7_audit/eq7_fullrecord_recompute.py`) needs the withheld exports and is not part of the steps above. Eq. 6 and Eq. 7 evidence levels are explained in `EQ6_EQ7_VERIFICATION.md`.

## Fixed seeds
- Original Phase 2G notebook: random seeds fixed in the notebook; re-execution reproduces the stored p-values exactly.
- Independent re-implementations: association-test permutations 20261112, bootstrap 20260826; cross-response exact permutation 20261113; seasonal control 20261112; Eq. 7 stress tests 20261113. Their permutation p-values agree with the stored ones within Monte Carlo error and not bit for bit.

## Known gaps
See `MISSING_INPUTS_AND_PERMISSIONS.md`.
