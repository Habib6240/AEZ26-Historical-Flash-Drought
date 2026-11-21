# AEZ-26 High Barind Tract: historical flash-drought analysis (software)

Software supporting the manuscript **"Source-dependent flash-drought chronology and land–water responses in the High Barind Tract, Bangladesh, 2000–2025"** (Md. Ahsan Habib, Department of Civil Engineering, Bangladesh University of Engineering and Technology (BUET), Dhaka-1000, Bangladesh; ORCID 0009-0009-6932-0567). Version 1.0.2. Zenodo software record: https://doi.org/10.5281/zenodo.24213343 (concept DOI of all versions; version 1.0.1 has the version DOI 10.5281/zenodo.24213344). See `CHANGELOG.md`.

This is the **software** release (GitHub repository and the matching Zenodo software archive, which hold the same code and documentation). The derived datasets are **not** in this release; they are in a separate **Zenodo derived-dataset record** (`AEZ26_Historical_Flash_Drought_Derived_Data`) and are not duplicated here. To run the Python scripts, unzip the dataset record so that its `data/` folder sits next to `scripts/`.

The release covers only the analyses retained in the manuscript: event detection and the 39-event GLDAS catalogue; GLDAS–ERA5-Land chronology comparison; ERA5-Land soil-water storage (Eq. 6) and temperature, dew-point, VPD and relative humidity (Eq. 7); driver indicators; land–water responses (MOD16, MOD13, GRACE, JRC); FDR-controlled association tests; seasonal-control and consensus-event analyses; Figures 2–4 scripts. Predictability and future-climate analyses were carried out separately, are outside the scope of the manuscript, and are **not** part of this release.

## Layout
| Folder | Content |
|---|---|
| `gee/` | Google Earth Engine scripts: Phase 1A–1G extraction, the extended 1981–2025 ERA5-Land/CHIRPS extraction (Phase 7A), study-area geometry audit, Eq. 6/7 source-export, 23-pentad diagnostic and full-record (1981–2025) Eq. 7 export scripts. The private asset identifier is replaced by a placeholder. |
| `notebooks/` | The **original Colab notebooks** for Phases 2A, 2C (v3), 2D, 2E, 2F (v2 plus the final naming patch) and 2G, and the Phase 7A notebook with corrected documentation (`AEZ26_Phase7A_Extended_Robustness_ERA5Land_1981_2025_Analysis_AUTO_SAVE_Colab_FINAL_DOCS_CORRECTED.ipynb`). `notebooks/superseded/` holds a provenance collection (Phase 2C v1; the original Phase 7A FINAL notebook). See `notebooks/README.md`. |
| `scripts/` | Python code: independent detector and chronology audit, statistics, Eq. 6/7 audit, figure scripts (Figures 1–4), a staging script, a check that greedy and maximum one-to-one matching give identical onset-agreement counts (`scripts/detection/AEZ26_SI_verify_matching_v04.py`) and the QA runner. Several are **independent re-implementations** (labelled in `SCRIPT_REGISTER.md`). |
| `documentation/` | Pre-specification of the consensus analysis and its hash; `documentation/PHASE7A_INPUT_PROVENANCE.md`; `qc_records/` (QC notes of the extraction phases and of Phase 2C v3). |
| `metadata/` | Source-dataset register (provider terms as located), Figure 1 provenance. |
| `checksums/` | SHA-256 of every file in this release except the manifest itself. |
| root | `REPRODUCE.md`, `SCRIPT_REGISTER.md`, `DATA_DICTIONARY.md` (describes the files of the dataset record), `EQ6_EQ7_VERIFICATION.md`, `MISSING_INPUTS_AND_PERMISSIONS.md`, `NOTICE_THIRD_PARTY_ATTRIBUTION.md`, `QA_REPORT.md`, `qa_results.json`, licence files, citation metadata. |

## Two pentad tables, and what Phase 7A locks
Phase 7A locks the SHA-256 of **file B** (`588e505b…`), a legacy 40-event-annotated copy of the pentad table. The **canonical** Phase 2C v3 table (39-event annotation, used for the manuscript) is **file A** (`44f76cbf…`) and is in the dataset record. The two files differ only in four event-annotation columns that the Phase 7A code never reads, and file B is never the manuscript's catalogue. See `documentation/PHASE7A_INPUT_PROVENANCE.md`.

## Status and limitations (read before reuse)
- **Complete end-to-end reproducibility is not claimed.** Phase 2A (daily backbone), Phase 2E (native-time alignment) and Phase 2F (response metrics) **cannot be fully reproduced from this release**: the source extracts, the merge workflow of the chunked exports and several quality-control inputs are not redistributed or were not available (`MISSING_INPUTS_AND_PERMISSIONS.md`). Reproduction from the Phase 2C v3 pentad table onward is documented in `REPRODUCE.md`.
- **Original Phase 2C–2G notebooks are included.** Re-execution in a scratch environment reproduced the stored Phase 2C v3 pentad table and catalogues, the Phase 2D outputs and the nine Phase 2G outputs; Phases 2A, 2E and 2F were not re-run (`SCRIPT_REGISTER.md`). The Phase 2G notebook fixes its random seeds and reproduces the stored p-values exactly.
- **Phase 7A.** The corrected notebook changes documentation only (hash lock, code and thresholds unchanged). The Candidate Audit table of the stored outputs cannot be fully reproduced because two historical catalogue copies are unavailable.
- **Equation 6:** formula-level reproduction for all 3,285 pentads (maximum absolute difference 4.5 × 10⁻¹³ mm) and a source-level comparison of reduction pathways in 35 pentads (maximum offset 3.25 mm). **Equation 7:** recomputed offline from per-pixel ERA5-Land exports for all 3,285 pentads; the stored series differs by a quantified seasonal offset with no detected step or drift. Neither equation is described as fully validated; the per-pixel exports are withheld and the stored series cannot be regenerated without Earth Engine and the private zone asset (`EQ6_EQ7_VERIFICATION.md`).
- Figure 1 cannot be regenerated from this release (study-area polygon and Bangladesh outline are not redistributed).
- The Earth Engine scripts and the Colab notebooks were run by the author; they were **not** executed in the release QA (syntax checks only, except where `SCRIPT_REGISTER.md` states otherwise).
- **Licences.** MIT applies only to software files (`LICENSE`, `LICENSE_SCOPE.md`). The separate dataset record is offered under CC BY 4.0 (author-generated derived data only); third-party attribution requirements are in `NOTICE_THIRD_PARTY_ATTRIBUTION.md`.

## How to cite
Cite the software and the dataset record separately (`CITATION.cff`). Software: concept DOI 10.5281/zenodo.24213343, or the version DOI of the version used. Dataset record: version 1.0.1, DOI 10.5281/zenodo.24336842 (concept DOI 10.5281/zenodo.24336841). Repository: https://github.com/Habib6240/AEZ26-Historical-Flash-Drought.
