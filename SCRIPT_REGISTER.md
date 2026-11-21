# Script register

Execution status distinguishes: **author-executed in Earth Engine/Colab** (not re-run here), **executed in release QA** (run on 2026-11-14 in a temporary composite of this software release and the dataset record and compared with stored outputs) and **syntax-checked only**. Nothing is claimed as executed unless stated.

## Google Earth Engine scripts (`gee/`)

| Script | Phase | Inputs | Outputs | Execution status | Syntax check (node --check, syntax only) |
|---|---|---|---|---|---|
| `gee/AEZ26_Phase1A_CHIRPS_Final.txt` | Phase 1A | CHIRPS daily (EE) | regional daily series CSV | Author ran in Earth Engine (original code) | syntax OK |
| `gee/AEZ26_Phase1B_ERA5Land_Final_Chunked.txt` | Phase 1B | ERA5-Land HOURLY (EE) | regional daily ERA5-Land series incl. hourly-derived RH/VPD (constant 0.61078) | Author ran in Earth Engine (original code) | syntax OK |
| `gee/AEZ26_Phase1C_GLDAS_Final_Chunked.txt` | Phase 1C | GLDAS-2.1 Noah (EE) | regional GLDAS series | Author ran in Earth Engine (original code) | syntax OK |
| `gee/AEZ26_Phase1D_MOD16A2GF_Final.txt` | Phase 1D | MOD16A2GF (EE) | regional ET/PET series | Author ran in Earth Engine (original code) | syntax OK |
| `gee/AEZ26_Phase1E_MOD13Q1_FINAL.txt` | Phase 1E | MOD13Q1 (EE) | regional NDVI series | Author ran in Earth Engine (original code) | syntax OK |
| `gee/AEZ26_Phase1F_GRACE_Mascon_FINAL.txt` | Phase 1F | GRACE mascon (EE) | regional TWSA series | Author ran in Earth Engine (original code) | syntax OK |
| `gee/AEZ26_Phase1G_JRC_SurfaceWater_FINAL.txt` | Phase 1G | JRC GSW monthly history (EE) | regional surface-water series | Author ran in Earth Engine (original code) | syntax OK |
| `gee/AEZ26_StudyArea_Geometry_Audit_and_Export.txt` | Study area | private AEZ-26 asset | geometry audit/export | Author ran in Earth Engine (original code) | syntax OK |
| `gee/AEZ26_Phase7A_Extended_Robustness_ERA5Land_CHIRPS_1981_2025_CHUNKED.txt` | Phase 7A | ERA5-Land DAILY_AGGR, CHIRPS (EE) | nine five-year pentad chunks (1981–2025) | Author ran in Earth Engine (original code); the archived Eq. 6/7 pathway | syntax OK |
| `gee/AEZ26_Eq6_Eq7_Source_Export_Script_v01.js` | Eq 6/7 closure | ERA5-Land (EE) | Part A: nine layer chunks; Part B: 45 per-pixel yearly files | Part A run by the author; Part B never run (header "NOT YET RUN" is stale for Part A) | syntax OK |
| `gee/AEZ26_Eq7_PartB_PILOT_2000.js` | Eq 6/7 closure | ERA5-Land (EE) | one-year (2000) per-pixel export | Run by the author for 2000; output not included | syntax OK |
| `gee/AEZ26_Eq7_Temporal_Robustness_DIAGNOSTIC_v02.js` | Eq 6/7 closure | ERA5-Land (EE) | 23-pentad A/B/C comparison CSV | Run by the author; export included | syntax OK |
| `gee/AEZ26_Eq7_FullRecord_SourceExport_v01.js` | Eq 6/7 closure (v1.0.1) | ERA5-Land DAILY_AGGR (EE) | pixel weights; 45 per-pixel yearly T/Td exports (withheld); 12-pentad A/B/C CSV (released) | Run by the author on 2026-11-15 (all three modes); not run in QA | syntax OK |

Dependencies: an Earth Engine account and a user-created FeatureCollection for the AEZ-26 polygon (the original asset identifier was replaced by a placeholder). Output chunks are written to Google Drive and merged outside Earth Engine.

## Notebooks (`notebooks/`)

All run by the author in Colab (originals, stored without outputs; each passed a syntax check in release QA, 0 errors). "Re-run" = executed in a scratch environment (not Colab) on 2026-11-14 with a harness that executes the notebook's code cells with Drive paths redirected; library versions differ from the Colab runs (see `QA_REPORT.md`).

| Notebook | Phase | Re-run evidence |
|---|---|---|
| `AEZ26_Phase2A_Daily_Backbone_AUTO_SAVE_Colab.ipynb` | 2A | Not re-run (source extracts and merge workflow unavailable): **cannot be fully reproduced** |
| `AEZ26_Phase2C_Flash_Drought_Detection_v3_FIRST_CROSSING_FIX_Colab.ipynb` | 2C v3 | Re-run from the stored backbone: pentad table and catalogues byte-identical to stored files |
| `AEZ26_Phase2D_Compound_Driver_Characterization_AUTO_SAVE_Colab.ipynb` | 2D | Re-run: the nine outputs matched |
| `AEZ26_Phase2E_Native_Response_Alignment_AUTO_SAVE_Colab.ipynb` | 2E | Not re-run (QC inputs unavailable): **cannot be fully reproduced** |
| `AEZ26_Phase2F_Native_Response_Metrics_Lag_AUTO_SAVE_Colab_v2.ipynb`, `AEZ26_Phase2F_FINAL_Naming_QC_Patch_Colab.ipynb` | 2F | Not re-run (depends on 2E link tables): **cannot be fully reproduced** |
| `AEZ26_Phase2G_Driver_Response_Statistical_Synthesis_AUTO_SAVE_Colab.ipynb` | 2G | Re-run: all nine outputs reproduced; seeds fixed in the notebook, stored p-values reproduced exactly |
| `AEZ26_Phase7A_..._FINAL_DOCS_CORRECTED.ipynb` | 7A | Re-run with file B, sanitised chunks and the 39-row catalogue: eight QC gates passed; 15 of 16 data/text outputs and both figures reproduced (12 byte-identical, 3 numerically or structurally equivalent); Candidate Audit partly reproduced (`documentation/PHASE7A_INPUT_PROVENANCE.md`) |
| `superseded/` (Phase 2C v1; original Phase 7A FINAL) | provenance only | Not part of the reproduction path |

## Python scripts

| Script | Phase | Nature | Inputs | Outputs | Execution status |
|---|---|---|---|---|---|
| `scripts/detection/independent_detector_and_chronology_audit.py` | Phase 2C/7A | INDEPENDENT RE-IMPLEMENTATION of the first-crossing detector and chronology audit (the original Phase 2C v3 notebook is in `notebooks/`) | data/derived pentad and catalogue files | results/phase1_closure/chron_* | Executed in release QA (exit 0) |
| `scripts/detection/AEZ26_SI_verify_matching_v04.py` | Chronology comparison (Sections 3.3, 4.2) | Verification script written 2026-11-21 (v1.0.2); compares the greedy one-to-one matching of the manuscript with an augmenting-path maximum matching and, if SciPy is installed, SciPy maximum bipartite matching; does not replace the greedy rule | the primary, OVERLAP26 and LONG45 catalogue CSVs under data/ | matching_verification_output/matching_comparisons.csv, matching_summary.json | Executed in the v1.0.2 candidate check (exit 0; 81 comparisons identical, observed counts 7/11/15 and 6/13/16 reproduced; exit 1 on a perturbed catalogue); not part of the v1.0.1 QA run |
| `scripts/statistics/association_tests_reproduction.py` | Phase 2G | INDEPENDENT RE-IMPLEMENTATION of the 46 association tests (the original Phase 2G notebook is in `notebooks/`; this script uses its own seed 20261112 and agrees with stored p-values within Monte Carlo error) | Phase2G/2F/2D derived files | assoc_reproduction.csv | Executed in release QA (exit 0) |
| `scripts/statistics/consensus_event_analysis.py` | Consensus analysis | Original analysis code written for the pre-specified consensus analysis | catalogues, drivers, responses | consensus_* | Executed in release QA (exit 0) |
| `scripts/statistics/cross_response_exact_permutation.py` | Phase 2G | Re-estimate (2,000,000 permutations, seed 20261113) | Cross-response derived files | cross_exact.csv | Executed in release QA (exit 0) |
| `scripts/statistics/seasonal_control_audit.py` | Seasonal control | Audit script (checks 1–3) | Phase 2F links, catalogues | seasctl_* | Executed in release QA (exit 0) |
| `scripts/statistics/response_minimum_window_fraction.py` | Seasonal control | Post hoc check 4 | Phase 2F links | seasctl_timing_fraction.csv | Executed in release QA (exit 0) |
| `scripts/eq6_eq7_audit/eq6_reconstruction_audit.py` | Eq 6/7 closure | Written 2026-11-13 for the audit (not original analysis code) | nine layer chunks, stored Phase 7A table | eq6_pentad_comparison.csv, eq6_reproduction_summary.json | Executed in release QA (exit 0) |
| `scripts/eq6_eq7_audit/eq7_pathway_comparison.py` | Eq 6/7 closure | Audit script (2026-11-13) | 23-pentad export, stored Phase 7A table | pentad_comparison_23.csv, BA_overall.csv | Executed in release QA (exit 0) |
| `scripts/eq6_eq7_audit/eq7_percentile_and_drift_tests.py` | Eq 6/7 closure | Audit script (2026-11-13) | pentad_comparison_23.csv, stored Phase 7A table | pooled_year_to_year_sd.csv; drift regression printed to console | Executed in release QA (exit 0) |
| `scripts/eq6_eq7_audit/eq7_sm_catalogue_stress.py` | Eq 6/7 closure | Audit stress test (seed 20261113) | stored ERA5 SM series, primary catalogue | era5_catalogue_mc.json, era5_baseline.json | Executed in release QA (exit 0) |
| `scripts/eq6_eq7_audit/eq7_driver_flag_stress.py` | Eq 6/7 closure | Audit stress test (seed 20261113); uses z_repro.py | event driver table, pentad indicators | flag_montecarlo_measured_sd.csv | Executed in release QA (exit 0) |
| `scripts/eq6_eq7_audit/downstream.py` | Eq 6/7 closure | Audit script (2026-11-13); its earlier flag Monte Carlo output (earlier SD assumptions) is superseded and written to a separately named file | event driver table, annual indicators | flag_margins.csv, trend_drift_sensitivity.csv | Executed in release QA (exit 0) |
| `scripts/eq6_eq7_audit/eq6_35pentad_soilwater_offsets.py` | Eq 6/7 closure (v1.0.1) | Audit script (2026-11-16) | 35-pentad A/B/C table, stored series | eq6_35pentad_soilwater_offsets.csv | Executed in release QA |
| `scripts/eq6_eq7_audit/eq7_fullrecord_checks.py` | Eq 6/7 closure (v1.0.1) | Audit script (2026-11-15/16); combines the S1–S7 checks | 12- and 23-pentad exports, offline recomputation (zone level), stored series | eq7_fullrecord reference files (A/B/C 35 table, merged series, two JSON) | Executed in release QA |
| `scripts/eq6_eq7_audit/eq7_fullrecord_recompute.py` | Eq 6/7 closure (v1.0.1) | Audit script (2026-11-15) | **withheld** per-pixel exports and weights | AEZ26_Eq7_Recomputed_3285pentads.csv | Executed in a scratch environment (output byte-identical to the released file); **cannot be run from the releases** |
| `scripts/eq6_eq7_audit/z_repro.py` | Eq 6/7 closure | Helper (z-score reproduction); imported by exec | event driver table, pentad indicators | none (library) | Used by the executed scripts |
| `scripts/stage_flat_inputs.py` | Utility | Written for this release | data/<topic>/ files | data/derived/ (flat copy) | Used by the executed scripts |
| `scripts/qa/run_release_checks.py` | QA | Written for this release | whole repository | qa_results.json | Run to produce qa_results.json |

## Figure scripts

| Script | Execution status |
|---|---|
| `scripts/figures/AEZ26_Fig1_StudyArea_Workflow/` (Figure 1 v05) | NOT RUN (needs the study-area polygon and Bangladesh outline, which are not redistributed) |
| `scripts/figures/AEZ26_Fig2_Catalogue/` | exit 0 in release QA; PNG and SVG written; pixel comparison with the manuscript PNG was not repeated (the earlier QA found 1.4 % of pixels differing; cause not investigated) |
| `scripts/figures/AEZ26_Fig3_Source_Record_Robustness/` | exit 0 in release QA; as above (earlier QA: 0.2 % of pixels differ) |
| `scripts/figures/AEZ26_Fig4_LandWater_Response/` | exit 0 in release QA; as above (earlier QA: 1.9 % of pixels differ) |

## Comparison of re-executed outputs with stored outputs

| Stored file | Comparison |
|---|---|
| `closure_checks/assoc_reproduction.csv` | max numeric difference 0; non-numeric identical True |
| `closure_checks/chron_event_diagnosis.csv` | max numeric difference 0; non-numeric identical True |
| `closure_checks/chron_res.json` | identical |
| `closure_checks/consensus_associations.csv` | max numeric difference 0; non-numeric identical True |
| `closure_checks/consensus_comparisons.csv` | max numeric difference 0; non-numeric identical True |
| `closure_checks/consensus_driver_classes.csv` | max numeric difference 0; non-numeric identical True |
| `closure_checks/consensus_masks.json` | identical |
| `closure_checks/cross_exact.csv` | max numeric difference 0; non-numeric identical True |
| `closure_checks/seasctl_events.csv` | max numeric difference 0; non-numeric identical True |
| `closure_checks/seasctl_summary.csv` | max numeric difference 0; non-numeric identical True |
| `closure_checks/seasctl_timing_fraction.csv` | max numeric difference 0; non-numeric identical True |
| `eq6_eq7_verification/eq6/eq6_pentad_comparison.csv` | max numeric difference 0; non-numeric identical True |
| `eq6_eq7_verification/eq6/eq6_reproduction_summary.json` | identical |
| `eq6_eq7_verification/eq7/BA_overall.csv` | max numeric difference 0; non-numeric identical True |
| `eq6_eq7_verification/eq7/era5_baseline.json` | identical |
| `eq6_eq7_verification/eq7/era5_catalogue_mc.json` | identical |
| `eq6_eq7_verification/eq7/flag_margins.csv` | max numeric difference 0; non-numeric identical True |
| `eq6_eq7_verification/eq7/flag_montecarlo_measured_sd.csv` | max numeric difference 0; non-numeric identical True |
| `eq6_eq7_verification/eq7/pentad_comparison_23.csv` | max numeric difference 0; non-numeric identical True |
| `eq6_eq7_verification/eq7/pooled_year_to_year_sd.csv` | max numeric difference 0; non-numeric identical True |
| `eq6_eq7_verification/eq7/trend_drift_sensitivity.csv` | max numeric difference 0; non-numeric identical True |

Paths in the comparison table are relative to `data/statistical_outputs/` (for `closure_checks/`) and `data/` (for `eq6_eq7_verification/`) in the derived-dataset record.

Notes: dependencies are in `requirements.txt`. Script READMEs in `scripts/*/README.md` give further detail. Scripts that read `data/derived/` need `scripts/stage_flat_inputs.py` first. `scripts/tables/README.md` documents that the table-building scripts for Tables 1–4 and S1–S6 are not part of this release. Stored comparison files are in the dataset record (`data/statistical_outputs/closure_checks/`, `data/eq6_eq7_verification/`). The Phase 7A GEE script and notebook, and Phases 2A, 2E, 2F: see `REPRODUCE.md`.
