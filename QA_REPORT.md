# Repository QA report: AEZ26_Historical_Flash_Drought v1.0.2 (software release candidate; not published)

Three full runs on 2026-11-21 all exited 0 with identical check results; the last ran 09:52:50–09:56:31 UTC (3 min 41 s) on this release as shipped, except that this paragraph was reworded afterwards and `checksums/SHA256SUMS.txt` regenerated with `python3 scripts/qa/run_release_checks.py` in a clean copy of this release with the derived-dataset record (v1.0.1) unzipped so that `data/` sits next to `scripts/`. Exit status 0; stdout 6,001 bytes, stderr empty. Machine-readable results: `qa_results.json`. Environment: Python 3.13.18, numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, matplotlib 3.11.2, Node 22 (syntax checks only), Linux. The v1.0.1 QA report and results are kept unchanged as `documentation/QA_REPORT_v1.0.1.md` and `documentation/qa_results_v1.0.1.json`; they are **not** evidence for v1.0.2.

## Checks passed
| Check | Result |
|---|---|
| Python syntax | 24 files, 0 errors (includes the new `scripts/detection/AEZ26_SI_verify_matching_v04.py`) |
| Notebooks | 10 notebooks, 0 syntax errors, 0 stored outputs |
| GEE JavaScript | 13/13 pass a `node` syntax check **only** (not executed in Earth Engine) |
| JSON / CSV | 10 JSON valid (one is the retained v1.0.1 results file); 92 CSV (software plus dataset composite), none empty or malformed |
| Private IDs / credentials | none found |
| Duplicate files | none |
| Manifest `checksums/SHA256SUMS.txt` | 94 entries, 0 mismatches |
| Re-execution of released Python scripts | 14/14 exit 0; 26/26 stored outputs identical (max numeric difference 0) |
| Figures 2–4 scripts | run (exit 0); PNG and SVG written |

## Matching-verification script (not part of the runner)
`scripts/detection/AEZ26_SI_verify_matching_v04.py` is not in the runner's list. It was run separately from an extracted copy of this release (log in the Stage 5 evidence): exit 0, 81 comparisons identical, observed onset agreement 7/11/15 and 6/13/16, null means 1.16/4.28/6.96, outputs byte-identical to the Stage 4.1 reference; a perturbed catalogue gives exit 1.

## Findings to read honestly
1. **Not reproducible end to end.** Phases 2A, 2E and 2F cannot be reproduced from the releases; Earth Engine extractions were not re-run; per-pixel Eq. 7 exports are withheld (see `MISSING_INPUTS_AND_PERMISSIONS.md`, `EQ6_EQ7_VERIFICATION.md`).
2. **Figure 1 was not run** (study-area polygon and Bangladesh outline are not redistributed).
3. **Scan for terms of removed components.** 4 files contain such terms only as historical notes: `scripts/figures/AEZ26_Fig1_StudyArea_Workflow/make_AEZ26_Fig1_v05.py`, its README, the Figure 3 README and `documentation/QA_REPORT_v1.0.1.md`. No removed-component data, code or tables are included.
4. **Historical v1.0.1 record.** The `qa_results.json` shipped in v1.0.1 lists 117 manifest entries, 93 CSV and 10 JSON files, whereas the v1.0.1 manifest has 89 entries; it was produced on a composite that differs from the shipped state. This is why v1.0.1 QA evidence is not reused.
5. Findings 2, 3, 7 and 8 of `documentation/QA_REPORT_v1.0.1.md` (Candidate Audit, Phase 7A input file, provider terms, missing pentad table) concern unchanged inputs and were not re-assessed here.

## Claims not made
Complete reproducibility; journal-tier status; any DOI or permission not verified. Nothing has been published or uploaded. The version DOI of v1.0.2 does not exist yet.
