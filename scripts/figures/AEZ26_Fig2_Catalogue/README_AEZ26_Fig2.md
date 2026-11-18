# README — AEZ-26 Main Figure 2 (Primary flash-drought catalogue and event characteristics)

## Scientific purpose
Descriptive historical figure for Results Section 4.1: (a) when the 39 primary regional flash-drought events occurred in 2000–2025, (b) their seasonal concentration, (c) their duration–severity structure by primary forcing class.
It is NOT a trend figure and shows no spatial footprints, grid-cell frequency or causal attribution.

## Source files (read directly; no event rows typed by hand)
| File | Rows | Use |
|---|---|---|
| AEZ26_Flash_Drought_Event_Catalogue_Primary_2000_2025.csv | 39 | panel a, c (timing, duration, severity); canonical Phase 2C v3 first-crossing-corrected primary catalogue |
| AEZ26_Phase2D_Event_Driver_Characterization.csv | 39 | forcing class, season label, secondary flags (QA only) |
| AEZ26_Phase2D_Seasonal_Onset_Summary.csv | 4 | cross-check of season counts |
| AEZ26_Phase2D_Driver_Class_Summary.csv | 4 | cross-check of class counts |
| AEZ26_Manuscript_Results_S4.1_to_S4.6_CONSOLIDATED_v01.docx | – | not used by the script; manuscript cross-check only (see "Not verified") |

## Authoritative v3 status
Catalogue has 39 rows, one `catalogue` value (PRIMARY_SM0_100), 0 right-censored events, and none of the six superseded v2 onset cases (2003_P49, 2017_P47, 2019_P34, 2022_P45, 2023_P26, 2024_P48). The script stops if the row count is not 39 or any of these appear. Nothing was filtered or reconstructed.

## Columns actually used
Catalogue: `event_id`, `onset_pentad`, `onset_start_date`, `onset_mid_date`, `event_end_date`, `onset_month`, `total_duration_pentads`, `total_duration_actual_days`, `severity_40pct_deficit_pp_pentads`, `intensification_duration_pentads`, `mean_intensification_rate_pp_per_pentad`, `right_censored_flag`, `prolonged_after_flash_flag`.
Driver file: `event_id`, `onset_season`, `primary_driver_class`, and the seven `*_flag` columns (QA counts only), plus the shared fields listed under join validation.

## Event join key
`event_id` (e.g. PRIMARY_SM0_100_FD_001). Join is one-to-one, 39/39, 0 unmatched. Validation: the two event_id sets are identical, and onset_pentad (also unique in both files), onset_mid_date, onset_year, onset_month, threshold_crossing_pentad, intensification_duration_pentads, total_duration_pentads, severity, mean intensification rate and prolonged flag agree for all 39 events. No fallback join on onset_pentad was needed.
Onset/end intervals were checked and none of the 39 events overlap.

## Derived variables
- Bar/line extent in panel a: `onset_start_date` to `onset_start_date + total_duration_actual_days`. This matches `event_end_date` to within the pentad convention (checked on the first rows; the source `event_end_date` is a pentad mid-date).
- Panel a row = `onset_month` (January at top). Rows are a layout device to separate events; the time axis is the calendar axis.
- Season derived from `onset_month`: DJF = Dec–Feb, MAM = Mar–May, JJAS = Jun–Sep, ON = Oct–Nov. Asserted identical to the source `onset_season` label for all 39 events and to the Seasonal_Onset_Summary counts.
- Duration = `total_duration_pentads`; severity = `severity_40pct_deficit_pp_pentads` (percentile-point pentads; definition as in the project's source documents — not re-derived here, VERIFY wording against the Methods text).

## Forcing-class definitions (source column `primary_driver_class`)
compound_Pdeficit_highPE = Compound; precipitation_deficit_only = Precipitation-only; high_PE_only = High-PE-only; neither_large_anomaly = Neither (neither primary large-anomaly threshold crossed; not absence of forcing). Classes describe conditions coincident with the rapid-intensification interval; not causal.
Encoding (colour + marker): Compound vermillion #D55E00 circle; Precipitation-only blue #0072B2 square; High-PE-only orange #E69F00 triangle; Neither white-filled diamond. Okabe–Ito palette; shapes keep classes distinguishable in grayscale.

## Linear vs log severity axis
Both were rendered and inspected during development. Linear (0–2100): 36 of 39 events fall in roughly the lowest 15% of the axis (severity < ~300), so the ordinary events are compressed and unreadable. Log: all 39 events and the extreme 2015_P55 remain visible and the majority is readable. Log was chosen after this visual comparison (not automatically) and is labelled "log scale" on the axis. Duration axis is linear.

## Display-only offset
11 points share exactly coincident (duration, severity) coordinates with at least one other event; they are shifted horizontally by ≤ 0.83 pentad for visibility. Plotted data values and all statistics are unchanged.

## QA results (all asserted in the script; source-derived)
- 39 events, 39 unique IDs, 0 duplicates, 0 right-censored, 0 overlaps, 0 missing plotted values, join 39/39.
- Season: MAM 9 (23.08%), JJAS 24 (61.54%), ON 5 (12.82%), DJF 1 (2.56%). Months: Sep 8, Apr 6, Jul 6; Jan, Nov, Dec 0.
- Duration: 3–58, median 5, IQR 3–6.5, 16 events = 3 pentads.
- Severity: 31.54–1958.46, median 104.62, IQR 62.31–158.08.
- Rapid intensification: 1–8 pentads, median 2. Mean intensification rate: 5.77–53.85, median 14.10.
- Prolonged (flag = 1): 2011_P56 (19), 2014_P55 (19), 2018_P53 (30), 2015_P55 (58). Top severity: 2015_P55 1958.46, 2018_P53 961.54, 2011_P56 544.62.
- Classes: compound 10, precipitation-only 10, high-PE-only 8, neither 11 (total 39).
- Secondary flags (QA only, not plotted): low RH 20, high VPD 18, high net radiation 16, high temperature 14, high wind 10. Note: the driver file's `large_PE_anomaly_flag` sums to 18 and was not part of the locked targets.

## Outputs
- PNG: 4134 × 2929 px, 175.006 mm × 124 mm at 600 dpi, RGB, white background, no alpha channel (alpha removed after rendering). Stored pHYs = 600 dpi (reported by Pillow as 599.9988, i.e. 23622 px/m).
- SVG: text kept as editable text (`svg.fonttype = none`); fixed hash salt and no date metadata; reruns give byte-identical SVG and PNG on the same software versions.
- Font: requested family list Arial → Liberation Sans → Helvetica → DejaVu Sans → generic sans-serif. This build had no Arial, so Liberation Sans (Arial-metric-compatible) was used for the PNG. The SVG stores the family list, so a viewer with Arial will render Arial.
- Sizes: panel letters 10 pt bold; axis labels 7.5 pt; tick labels 6.5 pt; event labels 6.5 pt bold; smallest annotation text 5.5 pt (median labels), at final 175 mm width.
- Versions: Python 3.12.3, matplotlib 3.10.8, pandas 3.0.2, numpy 2.4.4, Pillow 12.1.1.

## Reproduce
`python make_AEZ26_Fig2.py --data-dir <folder with the four CSVs> --out-dir <folder>` (CSVs are also searched in the script folder and the current directory). `--yscale linear` reproduces the rejected development view.

## Interpretation limits
Descriptive only. Regional (AEZ-wide) events, not spatial footprints or grid-cell frequencies. No trend inference from the chronology; seasonal counts are not a hypothesis test. Forcing class is not causal attribution and does not determine duration or severity; "neither" is not absence of atmospheric forcing. Labels such as 2015_P55 are onset pentads (year_pentad number).

## Not verified here
The manuscript .docx and the figure blueprint .docx were uploaded but were not parsed by the script; cross-checking of manuscript prose against the figure values is still to be done outside this package.
