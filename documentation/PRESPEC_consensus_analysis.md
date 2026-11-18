# Pre-specification of the consensus-event sensitivity analysis (written before any calculation)
Written 2026-11-12, before the analysis script was run. Its SHA-256 is recorded in the output.

## Matching rule
1. Catalogues: GLDAS primary (39 events) and the ERA5-Land source-only catalogue OVERLAP26 (2000–2025, same climatology length, 44 events), from the stored catalogue files.
2. Onset ordinal = year × 73 + pentad_of_year of the onset pentad.
3. One-to-one greedy matching in increasing absolute ordinal difference (ties broken by catalogue order), as in the stored Phase 7A agreement script. Each event is used at most once.
4. **Primary consensus set C**: GLDAS events matched at a tolerance of ±2 pentads. The complement N is the other GLDAS events. (±2 pentads = 10 days, the largest tolerance already reported in the manuscript.)
5. Sensitivity sets: ±1 and exact matches against OVERLAP26; ±2 matches against LONG45 restricted to onsets in 2000–2025.

## Quantities compared between C and N (all reported, no selection)
Season (JJAS share), total duration, severity, mean intensification rate, driver-class counts; for each of the four response products the response depth, event-weighted anomaly, minimum anomaly and lag to minimum; and the 16 primary driver–response Spearman coefficients with 95% percentile bootstrap intervals (2,000 resamples, seed 20260826) within C, set beside the full-sample coefficients.

## Tests
Mann–Whitney U (two-sided) for continuous variables, Fisher exact test for the JJAS share, chi-square-free description for driver classes (counts only). All p-values are nominal and descriptive; Benjamini–Hochberg q over the full comparison list is reported alongside. With n(C) small, absence of a difference is not evidence of equality.

## Interpretation rule (fixed in advance)
A full-sample conclusion is called "unchanged in the consensus set" if the estimate in C has the same sign and the full-sample estimate lies inside the C bootstrap interval. If not, it is called "not reproduced in C", and the result is reported as unfavourable to that conclusion whichever way it points. A null (no association) stays a null whenever the C interval includes zero.

## Chance-agreement benchmark (also fixed in advance)
To judge whether onset agreement exceeds seasonal coincidence, the ERA5-Land onset sequence is shifted by whole years (k × 73 pentads, k = 1…25, circular over 2000–2025), which preserves the seasonal timing and breaks the year; matches at each tolerance are recounted for each shift. The observed count is compared with this distribution (empirical one-sided p = (1 + number of shifts with at least as many matches)/(1 + 25)).

## Addendum A (seasonal-control audit; written before running scripts that compute it)
The raw native product series are not in the workspace; only event-window records (pre-event context, event and post-event) are stored. A random-date placebo cannot therefore be built, and none is fabricated. Three bounded checks use only stored records:
1. Event-period mean anomaly (event-weighted z, already standardized against same-slot 2000–2025 climatology) against zero, two-sided Wilcoxon signed-rank and sign test per product.
2. Selection reference: the expected minimum of n independent standard normal anomalies, n = number of valid native records in the window used for z_min (Monte Carlo, 200,000 draws per n, seed 20261112). Independence is the extreme case; dependence between neighbouring records makes the true selection effect smaller, so this is an upper bound on the selection artefact, not an estimate.
3. Before-event negative control: the same excess (observed minimum minus the iid expected minimum) computed for the pre-event context records; paired Wilcoxon signed-rank of post-event against pre-event excess.
All results are reported whichever way they point.

## Addendum B (POST HOC, added after seeing Addendum A results)
Check 4, prompted by the observation that median lags to the minimum are close to half of the search-window length: for each event and product the position of the minimum as a fraction of the window (lag from onset divided by window length, window = onset to event end plus the post-event window of 64, 96, 365 and 180 d for MOD16, MOD13, GRACE and JRC). For a series with no structure the expected fraction is about 0.5. Two-sided Wilcoxon signed-rank of the fractions against 0.5. This check is exploratory and post hoc and is labelled as such wherever it is reported.
