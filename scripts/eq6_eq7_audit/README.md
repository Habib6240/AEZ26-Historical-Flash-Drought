# Eq. 6 / Eq. 7 audit scripts
All scripts here were written for the 2026-11-13 to 2026-11-16 closure audit and are **not** original analysis code. Run `python scripts/stage_flat_inputs.py` first (the older scripts read `data/derived/`). Outputs go to `results/`.
| Script | Needs | Notes |
|---|---|---|
| `eq6_reconstruction_audit.py` | layer chunks, stored table | formula-level reproduction of Eq. 6 (3,285 pentads) |
| `eq6_35pentad_soilwater_offsets.py` | `data/eq6_eq7_verification/eq7_fullrecord/AEZ26_Eq7_ABC_35pentads_with_offline.csv`, stored table | B − A soil-water offsets of the 35 pentads by month, period and state |
| `eq7_fullrecord_checks.py` | zone-level files in `eq7_fullrecord/`, 23-pentad export, stored table | S1–S7: agreement, pathway comparison, step, drift and trend checks; reproduces the reference outputs exactly |
| `eq7_fullrecord_recompute.py` | **withheld** per-pixel exports and weights table | cannot be run from the releases; run in a scratch environment, output byte-identical to the released recomputation |
| `eq7_pathway_comparison.py`, `eq7_percentile_and_drift_tests.py`, `eq7_sm_catalogue_stress.py`, `eq7_driver_flag_stress.py`, `downstream.py`, `z_repro.py` | see `SCRIPT_REGISTER.md` | 23-pentad analysis and stress tests (Tables S19/S20) |
