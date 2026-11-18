# README — AEZ-26 Main Figure 4 (Land–water responses and multiplicity-aware event-level inference)

## Scientific purpose
Show (a) product-specific response depth, (b) onset-to-minimum lag, (c) the full multiplicity-aware association summary (all source-backed tests, BH/FDR q-values), and (d) seasonal-normal recovery vs right-censoring, for the 39 primary flash-drought events. Supports Results Section 4.3. No causal cascade is inferred; no statistically established association is claimed; GRACE TWSA is not groundwater; JRC surface-water extent is not storage; right-censored ≠ permanent non-recovery.

## Source files (read directly)
Phase 2F: AEZ26_Phase2F_MOD16_Event_Response_Metrics.csv, _MOD13_Event_Response_Metrics.csv, _GRACE_TWSA_Event_Response_Metrics.csv, _JRC_SurfaceWater_Event_Response_Metrics.csv (39 rows each), _Cross_Response_Event_Synthesis.csv (39 rows, event-key check), _QC.csv.
Phase 2G: AEZ26_Phase2G_Primary_Driver_Response_Associations.csv (16), _Secondary_Atmospheric_Response_Associations.csv (12), _EventPhysics_Response_Associations.csv (8), _DriverClass_Response_Comparisons.csv (4), _Cross_Response_Coupling.csv (6), _Response_Cohort_Summary.csv (9 cohorts; median cross-check), _QC.csv.
Uploaded but not used: AEZ26_Phase2D_Event_Driver_Characterization_1.csv, AEZ26_Phase2D_QC.csv.

## Keys
Event key: `event_id` (unique and identical across all five 39-row event tables). Test key: `family | predictor | outcome` for primary/secondary/event-physics; `driver_class_omnibus | outcome` for the driver-class family; `cross_response | pair_label` for coupling. All 46 keys are unique.

## Columns used
Per product: `minimum_{ETPET|NDVI|TWSA|water_fraction}_drop_from_prebaseline_z`, `lag_onset_to_minimum_*_days`, `{PRODUCT}_seasonal_normal_recovery_censored_flag`, `{PRODUCT}_relative_days_from_event_end_to_seasonal_normal_recovery`, `{PRODUCT}_relative_days_from_event_end_to_prebaseline_recovery`, `{PRODUCT}_seasonal_normal_recovery_before_event_end_flag`, and `GRACE_/JRC_response_metric_available_flag`.
Statistics: `family`, `predictor`, `predictor_label`, `outcome`, `pair_label`, `n`, `rho`, `p_perm`, `p_fdr_bh`, `fdr_0_05_flag`, `epsilon2` (class family).

## Definitions
- Response depth (plotted) = z_base − z_min, computed as −(source column "…_drop_from_prebaseline_z"); the source column stores z_min − z_base, so a positive plotted depth = a decline from the pre-event baseline. Not clipped. Verified: recomputed medians equal the Phase 2G cohort-summary medians exactly. Depth is product-specific and not a cross-product drought-severity scale.
- Lag = stored `lag_onset_to_minimum_*_days` (confirmed by the authors): the elapsed time in days from flash-drought onset to the native observation date of the minimum standardized response identified within the locked onset-to-post-event context.
- Seasonal-normal recovery: observed when a recovery time is stored (recovery_censored_flag = 0); "right-censored / not observed within the finite window" when censored_flag = 1 (source terminology: censored; no interpolation or extrapolation per Phase 2F QC). Counts of observed recovery equal the number of stored recovery times (asserted). Pre-baseline recovery (not plotted; Supplement): observed/not = MOD16 28/11, MOD13 29/10, GRACE 23/12, JRC 14/18 (asserted). Seasonal-normal recovery before event end: 7, 4, 1, 1 (signed timing; QC: not a calculation error).
- Valid n: depth MOD16 39, MOD13 39, JRC 31, GRACE 34; lag MOD16 39, MOD13 39, JRC 32, GRACE 35; recovery status 39, 39, 32, 35. GRACE and JRC include only events with response metrics available (35 and 32). QC also records 22 GRACE and 11 JRC response minima as confounded; they are retained, not isolated responses.
- Native temporal support (confirmed by the authors from the project documentation; not stored in the CSVs): MOD16A2GF ≈ 8-day native composites; MOD13Q1 16-day native composites; GRACE/GRACE-FO irregular, approximately monthly native intervals; JRC Surface Water monthly. Timing precision is constrained by this native temporal support; no sub-composite timing precision is implied.

## Statistics
Families and row counts (source-confirmed): primary driver–response 16, secondary atmospheric 12, event physics 8, driver-class omnibus 4, cross-response coupling 6; total 46; duplicate test keys 0. FDR rule: q ≤ 0.05; `p_fdr_bh` is the Benjamini–Hochberg q-value computed within each family from `p_perm`; the script recomputes BH within each family and matches the stored values (max difference ≈ 1e-16). q ≤ 0.05 count = 0 across all 46 tests; minimum q = 0.0576 (the two cross-response pairs). Panel c plots q only (no p-values, no stars): one dot per test; rows are predictors, with up to four product-coloured dots per row (primary 4×4, secondary 3×4, event physics 2×4, driver-class 1×4); cross-response pairs are single grey dots.
Nominal cross-response pairs (annotated, not marked as significant): MOD16 vs NDVI n = 39, rho = +0.383, p = 0.0192, q = 0.0576 (bootstrap CI 0.058–0.653 in source); TWSA vs JRC n = 29, rho = +0.476, p = 0.0098, q = 0.0576 (CI 0.164–0.731). The other four pairs have p ≥ 0.119. Driver-class omnibus q = 0.8754 for all four outcomes; epsilon² = 0 (MOD16), 0 (MOD13), 0.0126 (GRACE), 0 (JRC). Interpretation: "No FDR-supported association was detected" — not "no relationship". Sample support differs by outcome (MOD16/MOD13 39, GRACE 34–35, JRC 31–32, cross pairs 29–39) and by family.

## QA performed (asserted in script)
Locked values matched with no discrepancy: depth medians 1.486 / 1.014 / 0.808 (GRACE) / 0.863 (JRC); lag medians 37 / 45 / 107 (JRC) / 193 (GRACE) days; recovery observed/censored 28/11, 28/11, 15/20 (of 35), 16/16 (of 32); negative depths retained (MOD16 2, MOD13 2, JRC 2, GRACE 3; minima −0.263, −0.952, −0.517, −0.477); stored q equals within-family BH; all QC rows PASS/RESULT.

## Outputs
PNG 4134 × 3307 px (175.006 × 140 mm), RGB, white, no alpha, stored 600 dpi (Pillow 599.9988 = 23622 px/m). SVG: editable text (svg.fonttype none), fixed hash salt, no date; reruns give byte-identical PNG and SVG. Font list Arial → Liberation Sans → Helvetica → DejaVu Sans; this build used Liberation Sans. Smallest text 5.4 pt. Jitter in a and b: fixed seed (4), vertical only. Products: MOD16 vermillion circle, MOD13 green square, JRC blue triangle, GRACE purple diamond (not SSP colours). Versions: Python 3.12.3, matplotlib 3.10.8, pandas 3.0.2, numpy 2.4.4, Pillow 12.1.1.
Reproduce: `python make_AEZ26_Fig4.py --data-dir <folder with the 13 CSVs> --out-dir <folder>`.

## Interpretation limits
Descriptive, event-level. No causal propagation (ET → vegetation → storage) is implied; products observe different processes at different native time steps; depths are not directly comparable across products; negative depths are valid values; nominal p < 0.05 results are not established; right-censored recovery does not mean non-recovery; recovery depends on definition and window.
