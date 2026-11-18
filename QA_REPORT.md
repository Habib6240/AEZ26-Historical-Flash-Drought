# Repository QA report: AEZ26_Historical_Flash_Drought v1.0.1 (software; not published)

Run on 2026-11-16 in a temporary composite of this release and the derived-dataset record (`data/` next to `scripts/`). Machine-readable results: `qa_results.json`; runner: `scripts/qa/run_release_checks.py`. Environment: Python 3.13.18, numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, matplotlib 3.11.2; node 22 (syntax checks only). No network access. Colab library versions differ.

## Checks passed
| Check | Result |
|---|---|
| Python syntax | 23 files, 0 errors |
| Notebooks | 10 notebooks (8 canonical, 2 superseded), 0 syntax errors, 0 stored outputs |
| GEE JavaScript | 13/13 pass a `node` syntax check **only** (not executed in Earth Engine here) |
| JSON / CSV | 10 JSON valid; 93 CSV (software composite incl. dataset), none empty or malformed |
| Private IDs / credentials | none found (private asset identifier replaced by `projects/<YOUR-EE-PROJECT>/assets/<YOUR-AEZ26-ASSET>`) |
| Re-execution of released Python scripts | 14/14 exit 0; 26/26 stored outputs identical (max numeric difference 0; Eq. 6: 3,285 pentads, max abs diff 4.5e-13 mm) |
| Original notebooks (scratch re-run, separate from the runner) | 2C v3, 2D, 2G reproduced stored outputs; 7A reproduced 15 of 16 data/text outputs and both figures; see `SCRIPT_REGISTER.md` |
| Figures 2–4 scripts | run (exit 0) and write PNG and SVG |

## Findings to read honestly
1. **Not reproducible end to end.** Phases 2A, 2E and 2F cannot be fully reproduced from the releases (missing source extracts, merge workflow and QC inputs; `MISSING_INPUTS_AND_PERMISSIONS.md`). Phase 1 extraction and Earth Engine scripts were not executed here (the full-record Eq. 7 export script was run by the author on 2026-11-15; exports hashed, not re-run).
2. **Candidate Audit.** The stored Phase 7A Candidate Audit has three rows; only the 39-row catalogue copy is available (SHA-256 `e524a485…`). The 40-row (`69c8dc0c…`) and 45-row (`db6e218b…`) copies are unavailable, so that table is reproduced only in part. No row was recreated.
3. **Phase 7A input.** The notebook locks file B (`588e505b…`), a legacy 40-event-annotated pentad table, not the canonical 39-event table (file A, `44f76cbf…`); the Phase 7A code never reads the differing columns. Colab and scratch library versions differ; results differ only at floating-point level (14th digit) or in formatting of signed zeros.
4. **Figures.** Figure 1 was not run (study-area polygon and Bangladesh outline are not redistributed). Regenerated Figures 2–4 were compared with the manuscript images on 2026-11-16: same size, sub-pixel registration, and at most 0.08 % of pixels outside a 3-pixel tolerance (anti-aliasing at text and line edges). Figure 3 differed in one label ("SOURCE26" instead of "OVERLAP26"); the label was corrected in the script, caption and README, after which no pixel lies outside the tolerance.
5. **Eq. 6 and Eq. 7.** Eq. 6: formula-level reproduction of 3,285 pentads and a 35-pentad source-level comparison. Eq. 7: offline recomputation for 3,285 pentads from per-pixel exports that are withheld; the recomputation script cannot be run from the releases, so only its zone-level outputs and the checks on them are re-executed here (`EQ6_EQ7_VERIFICATION.md`). Neither equation is described as fully validated.
6. **Excluded-analysis term scan.** Four files mention removed components only as historical notes (Figure 1 script and README, Figure 3 README, this report). No predictability, future-climate or early-warning data, code or tables are included.
7. **Provider terms** were read from Earth Engine catalogue pages (secondary sources); the ERA5-Land and GLDAS-2.1 primary documents were not read. The author must confirm before deposit.
8. A pentad table with SHA-256 `d397…` was never found.

## Executed versus documented only
Executed here: Python syntax, notebook syntax, JSON/CSV parsing, manifest verification, private-identifier and credential scan, re-execution of the released scripts (including the two new Eq. 6/7 check scripts) with output comparison, Figure 2–4 scripts. Documented only: Earth Engine scripts (syntax only), Phase 1 extraction, Figure 1, the full-record Eq. 7 recomputation from withheld per-pixel exports, pixel equality of Figures 2–4.

## Claims not made
Complete reproducibility; journal-tier status; any DOI, licence for data, or permission not verified. Nothing has been published or uploaded.

## Scope of this report
Cross-release checks (identity of the GitHub and Zenodo software trees, manifests, scans, reference resolution) and manuscript/supplementary checks are in the separate final QA report delivered with the releases, because a report inside an archive cannot contain that archive's own hash.
