# Phase 7A input table: canonical file A and historical locked input B

Two versions of `AEZ26_Pentad_Hydroclimate_Indicators_2000_2025.csv` exist. They have the same name, 1,898 rows and 59 columns, and must not be confused.

| | File A (canonical) | File B (historical Phase 7A locked input) |
|---|---|---|
| SHA-256 | `44f76cbf8a66758087ffb5b708e5897a1f3c86a4f4726f6f66b5dbea64dfe9b3` | `588e505b9d33769f9146c289e75edda1948eb80e00d57b100b9f1776fc72e4b4` |
| Size | 1,569,812 bytes | 1,569,636 bytes |
| Event annotation | 39 events (`PRIMARY_SM0_100_FD_001`–`039`) | 40 events (adds `PRIMARY_SM0_100_FD_040`; legacy annotation) |
| Role | The Phase 2C v3 pentad table; byte-identical to a fresh re-run of the Phase 2C v3 notebook; supports the manuscript's 39-event catalogue | The file whose SHA-256 is locked in the original Phase 7A FINAL notebook (`LOCKED_GLDAS_PENTAD_SHA256`) |
| Location in the dataset record | `data/pentad_indicators/` | `historical_inputs/phase7a_locked_input/` |

**Differences.** A and B differ in 280 cells across 211 rows, only in the four columns `primary_flash_drought_event_flag` (32 cells), `primary_flash_drought_event_id` (211), `primary_flash_drought_intensification_flag` (26) and `primary_flash_drought_drought_phase_flag` (11). Every other column, including `SM_0_100_pct`, is identical. B's event IDs are a superset of A's.

**What the Phase 7A code uses.** The Phase 7A notebook never reads the four annotation columns (the text `primary_flash_drought` does not occur in it). It re-detects events from `SM_0_100_pct` with the frozen first-crossing detector and requires the reconstruction to contain exactly 39 events. The legacy 40-event annotation was therefore not used in any Phase 7A calculation, and it is not the manuscript's event catalogue. File B must never be described as the canonical 39-event table.

**Provenance.** The original notebook described the locked hash as "the Phase-2C v3 pentad table". That description is inaccurate; it is corrected in `AEZ26_Phase7A_Extended_Robustness_..._FINAL_DOCS_CORRECTED.ipynb` (documentation-only change; the lock, code and thresholds are unchanged). Where B came from is not confirmed. Its 40-event annotation matches the row count of an earlier 40-row Phase 2C catalogue (SHA-256 `69c8dc0cb664b2dd79f9311e2db51718a614fa3069269dc692dd05f89e929292`), but that catalogue file was not available for comparison, so the link is a hypothesis. A third pentad-table version reported with a hash beginning `d397` was not found and was not compared.

**Running Phase 7A.** The notebook finds the pentad table by file name under its `BASE` folder and accepts only a copy whose SHA-256 equals the locked value. Place file B (and, if you like, file A in another folder; it is ignored by the lock) under `BASE`, place the nine sanitised chunks from `data/phase7a_chunks_sanitized/` under `BASE`, and place `AEZ26_Flash_Drought_Event_Catalogue_Primary_2000_2025.csv` (39 rows) from `data/event_catalogue/` under `BASE`.

**Validation (2026-11-14, scratch environment, not Colab).** With these inputs the corrected notebook passed all eight QC gates (3,285 rows; 45 years; at least 73 pentads per year; no incomplete pentads; no missing core values; 39 reconstructed events; no detector-logic violations in either record) and reproduced 11 of the 15 stored data and text outputs byte for byte. The four others are not byte-identical for stated reasons: `AEZ26_Robustness_Continuous_State_Agreement.csv` (p-values differ in the 14th significant digit, scipy version), `AEZ26_Robustness_Long_Record_Trend_Diagnostics.csv` (signed zero, numpy version), `AEZ26_Robustness_Environment_and_Hashes.json` (library versions; chunk hashes refer to the sanitised chunks, see `CHUNK_HASH_MAP.csv`; candidate counts) and `AEZ26_Phase7A_GLDAS_Primary_Candidate_Audit.csv` (see below). The original, unmodified notebook run on the original raw chunks reproduced the same files with the same four exceptions.

**Known limitation: Candidate Audit.** The stored `AEZ26_Phase7A_GLDAS_Primary_Candidate_Audit.csv` lists three same-named catalogue copies (40 rows `69c8dc0c…`, 45 rows `db6e218b…`, 39 rows `e524a485…`). Only the 39-row copy is available, so a re-run lists one candidate and cannot reproduce the two stale rows. The stored file is released as the record of that audit. This limitation remains open.

**Sanitisation.** The Phase 7A chunks and the notebook originally carried the private Earth Engine asset identifier. In this release it is replaced by `projects/<YOUR-EE-PROJECT>/assets/<YOUR-AEZ26-ASSET>`; no other value was changed (checked column by column).
