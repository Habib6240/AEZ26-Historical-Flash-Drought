# README — AEZ-26 Main Figure 3 (Source and record-length robustness of regional flash-drought detection)

## Scientific purpose
Robustness/sensitivity figure: (a) how event counts change with soil-moisture source and record length, (b) how exact onset chronology depends on source, (c) that broad seasonal structure is comparatively more stable than exact dates, (d) that the extended 1981–2025 ERA5-Land record shows no FDR-supported increase in event frequency. Supports Results Section 4.2. ERA5-Land is a sensitivity catalogue and does not validate or invalidate GLDAS; source disagreement is not read as error; no inventory is "ground truth".

## Source files (read directly; no typed values)
AEZ26_Phase7A_Audit_Reconstructed_GLDAS_v3_Primary_39.csv (39 rows; GLDAS primary), AEZ26_Robustness_ERA5Land_Source26_Event_Catalogue_2000_2025.csv (44), AEZ26_Robustness_ERA5Land_Long45_Event_Catalogue_1981_2025.csv (74), AEZ26_Robustness_Event_Onset_Agreement.csv (6 rows), AEZ26_Robustness_Long45_Seasonality.csv (4), AEZ26_Robustness_Long45_Period_Event_Rates.csv (3), AEZ26_Robustness_Continuous_State_Agreement.csv (2), AEZ26_Robustness_Long_Record_Trend_Diagnostics.csv (5), AEZ26_Robustness_QC.csv (8 checks, all PASS). AEZ26_Phase7A_Corrected_Robustness_Summary.md was read as a cross-check only (39/44/74/43 events and the onset-agreement counts agree).

## Inventories and common-period restriction
GLDAS primary (catalogue PRIMARY_SM0_100): 39 events, 2000–2025, locked Phase 2C v3 chronology. ERA5-Land OVERLAP26 (labelled SOURCE26, catalogue id ERA5_SOURCE26, in the archived project files; the figure and manuscript use OVERLAP26): 44 events, 2000–2025. ERA5-Land LONG45 (ERA5_LONG45): 74 events, 1981–2025; restricted to onset_year 2000–2025 by the script = 43 events. Event IDs and onset pentads are unique in all three catalogues; no duplicate rows. Panel a keeps 39/44/43 (common period) and 74 (extended record) in separate, labelled groups.

## Onset agreement (panel b)
Source: matched_primary_events by tolerance_pentads (0, 1, 2) for GLDAS_primary_vs_ERA5_source26 (7, 11, 15 of 39; 44 sensitivity events) and GLDAS_primary_vs_ERA5_long45_overlap (6, 13, 16 of 39; 43 sensitivity events). The counts are cumulative (matched within ≤ tolerance; non-decreasing, asserted), one-to-one. The script independently re-derives them as maximum one-to-one matchings of onset pentads (onset index = year × 73 + pentad number) within 0/1/2 pentads, and reproduces 7/11/15 and 6/13/16 exactly. Percentages of 39 (summary.md): OVERLAP26 17.9/28.2/38.5%; LONG45 15.4/33.3/41.0%. The y-axis is truncated at 20 and annotated. Not an accuracy measure.

## Seasonality (panel c)
Season definitions (by onset month): DJF Dec–Feb, MAM Mar–May, JJAS Jun–Sep, ON Oct–Nov (source labels Winter_DJF, PreMonsoon_MAM, Monsoon_JJAS, PostMonsoon_ON). GLDAS counts derived from the primary catalogue: MAM 9, JJAS 24, ON 5, DJF 1 (n = 39) → 23.1, 61.5, 12.8, 2.6%. ERA5 LONG45 counts from the seasonality CSV (and confirmed against the catalogue): MAM 23, JJAS 44, ON 7, DJF 0 (n = 74) → 31.1, 59.5, 9.5, 0.0%. Shares use each source's own denominator; the two samples span different record lengths (2000–2025 vs 1981–2025), so this is a comparison of shares, not counts. No ERA5 OVERLAP26 seasonal shares are plotted. Derived there (not plotted): JJAS 28, MAM 12, ON 4.

## Period rates (panel d)
Stored periods (source labels): 1981-1995, 1996-2010, 2011-2025; events 25, 25, 24 over 15 years each → 1.67, 1.67, 1.60 events yr⁻¹ (events_per_year = events/years, asserted; counts re-derived from LONG45 onset years). ERA5-Land LONG45 only.

## Continuous-state agreement
Spearman rank correlation between ERA5-Land and GLDAS: percentile agreement ρ = 0.583; standardized-anomaly agreement ρ = 0.578 (n = 1,898 paired pentads over the common 2000–2025 period, 26 years × 73 pentads; confirmed from the Phase 7A documentation, not stored in this CSV; p-values ≈ 1e-173/1e-170 in the source, not plotted). It indicates moderate continuous-state agreement, not event-date agreement.

## Trend / FDR interpretation
The trend table (Theil–Sen slope per decade, 95% CI, Kendall τ, nominal Kendall p) holds five tests: ERA5-Land annual flash-drought count (slope 0.0 events/decade, 95% CI 0.0–0.0 — the Theil–Sen median slope and bounds are all exactly zero for this sparse count series; τ = −0.040, p = 0.735), mean temperature (+0.089 °C/decade, p = 0.0439), mean VPD (−0.0247 kPa/decade, p = 0.0528), CHIRPS precipitation (−26.8 mm/decade, p = 0.225), ERA5-Land potential evaporation (−42.0 mm/decade, p = 0.0210). The source table stores NO q-values. Benjamini–Hochberg q-values were computed in the script over those five stored p-values (the confirmed correction family; the q-values themselves are not stored in the source table): 0.0879 (temperature), 0.0879 (VPD), 0.0879 (potential evaporation), 0.281 (precipitation), 0.735 (event count); minimum 0.0879 > 0.05, so no tested trend survives FDR (consistent with the project target ≈ 0.0879). The BH correction family is confirmed from the Phase 7A documentation as these five parallel trend tests: annual flash-drought count, mean temperature, mean VPD, CHIRPS precipitation and ERA5-Land potential evaporation. Panel d shows only the event-count result and the "no tested hydroclimate trend survives FDR" conclusion; individual hydroclimate coefficients belong in the Supplement.

## QA performed (asserted)
Catalogue counts 39/44/74/43; unique keys; QC all PASS; onset matches (stored and re-derived); seasonal counts and LONG45 catalogue-vs-CSV agreement; period rates; ρ values; no recomputed BH q ≤ 0.05; trend values match the project context targets.

## Outputs
PNG 4134 × 2881 px (175.006 × 122 mm), RGB, white, no alpha (alpha removed after rendering), stored 600 dpi (Pillow 599.9988 = 23622 px/m). SVG: editable text (svg.fonttype none), fixed hash salt, no date; reruns give byte-identical PNG and SVG. Fonts: Arial → Liberation Sans → Helvetica → DejaVu Sans; this build used Liberation Sans. Smallest text 5.4 pt. Source encodings (identical across panels a–c; not a ranking): GLDAS blue circle, ERA5-Land OVERLAP26 orange square, ERA5-Land LONG45 green triangle (open triangle = full 1981–2025 record in panel a). Versions: Python 3.12.3, matplotlib 3.10.8, pandas 3.0.2, numpy 2.4.4, Pillow 12.1.1.
Reproduce: `python make_AEZ26_Fig3.py --data-dir <folder with the nine CSVs> --out-dir <folder>`.

## Interpretation limits
Broad seasonal structure and continuous-state behaviour are comparatively robust (more stable), whereas exact event chronology remains source- and record-length-sensitive. Not validation, not accuracy, not an error estimate for either source. No FDR-supported historical frequency trend is not evidence of no climate change and does not contradict future-risk analyses. Larger event counts do not imply a better catalogue.
