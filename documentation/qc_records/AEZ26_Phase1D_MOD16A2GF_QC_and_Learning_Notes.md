# Phase 1D — MOD16A2GF ET/PET: Final QC and Learning Notes

## Final status

**PASS — The native-composite MOD16A2GF ET/PET dataset for 2000–2025 was exported and internally validated.**

## Dataset QC

- Rows / composites: **1196**
- Coverage: **2000-01-01 to 2025-12-31**
- Duplicate composite starts: **0**
- Composite-duration mismatches: **0**
- Years with an incorrect 8-day start-date sequence: **0**
- Composite-day distribution: **{5.0: 19, 6.0: 7, 8.0: 1170}**
- Missing primary ET composites: **0**
- Zero strict-QA coverage composites: **35**
- Missing strict-QA ET composites: **35**

The strict-QA missing count matches the zero-coverage count, so strict-QA nulls are behaving as intended rather than being converted to zero.

## Formula checks

- Max error, primary ET composite / days = ET mm/day: **8.882e-16**
- Max error, primary PET composite / days = PET mm/day: **1.776e-15**
- Max error, strict ET composite / days = ET mm/day: **8.882e-16**
- Max error, strict PET composite / days = PET mm/day: **1.776e-15**
- Max error, primary ET/PET ratio: **2.220e-16**
- Max error, strict ET/PET ratio: **2.220e-16**

## Full-period ranges

- Primary ET: **0.1097 to 36.2607 mm/composite**
- Primary PET: **11.3497 to 79.4534 mm/composite**
- Primary ET rate: **0.0137 to 4.5326 mm/day**
- Primary PET rate: **2.2699 to 9.9317 mm/day**
- Primary ET/PET: **0.0015 to 0.8338**
- Primary valid fraction: **0.993268 to 0.993419**
- Strict-QA fraction: **0.000000 to 0.993419**, mean **0.510678**

## What I learned in GEE

- MOD16A2GF is preserved at its native ~8-day composite timing; it was not converted into synthetic daily observations.
- ET and PET use a scale factor of 0.1 and are retained both as mm/composite and as composite-total divided by actual composite length.
- Most composites are 8 days; the last annual composite is 5 days in common years and 6 days in leap years.
- The primary regional ET/PET ratio is `regional mean ET / regional mean PET`, not the mean of pixel-wise ET/PET ratios.
- The valid gap-filled MOD16A2GF series is the primary series.
- A deliberately strict QA mask is retained as a sensitivity/QC track. When it has zero spatial coverage, ET/PET remain null rather than becoming zero.
- QA coverage fractions are scientific metadata and should be carried into later analysis.

## Methodology record

MOD16A2GF Collection 6.1 ET and PET were processed at their native composite timing over AEZ-26. ET and PET were scaled by 0.1 and spatially averaged over the study geometry. A primary track used valid gap-filled product pixels, while a stricter sensitivity track required good MODLAND QA, clear cloud state and SCF quality <= 1. Composite totals and normalized per-day rates were retained. The actual number of days in each composite was calculated explicitly so that year-end 5- or 6-day composites were not treated as 8-day periods. Regional ET/PET was calculated as the ratio of the regional mean ET to regional mean PET. Missing strict-QA coverage was preserved as null and flagged rather than filled.
