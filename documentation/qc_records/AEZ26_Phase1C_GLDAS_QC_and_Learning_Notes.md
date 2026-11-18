# Phase 1C — GLDAS v2.1 Noah: Final QC and Learning Notes

## Final status

**PASS — The five GLDAS chunks were merged into one complete 2000–2025 daily dataset, with the known first-day state-snapshot edge case retained and flagged rather than filled.**

## Dataset assembly QC

- Final rows: **9497**
- Date range: **2000-01-01 to 2025-12-31**
- Missing calendar dates: **0**
- Duplicate dates: **0**
- Total missing cells: **0**
- State-image count distribution: **{7: 1, 8: 9496}**
- Flux-image count distribution: **{8: 9497}**
- Non-8 state days: **1**
- Non-8 flux days: **0**

### Known edge case

- `2000-01-01`: state images = **7**, state_complete_flag = **0**, complete_day_flag = **0**.

This first-day condition is retained as observed. No synthetic 00:00 state was created.

## Internal mathematical consistency

- Max error in `SM_0_10 + SM_10_40 = SM_0_40`: **5.684e-14 mm**
- Max error in `SM_0_40 + SM_40_100 = SM_0_100`: **1.705e-13 mm**
- Max error in `SM_0_100 + SM_100_200 = SM_0_200`: **3.411e-13 mm**
- Max error in `surface runoff + baseflow = total runoff`: **1.421e-14 mm/day**

## Full-period ranges

- `SM_0_10cm_mm`: min **10.4759**, max **39.6692**, mean **25.9615**
- `SM_10_40cm_mm`: min **41.4416**, max **119.3954**, mean **81.5042**
- `SM_40_100cm_mm`: min **83.4986**, max **242.2636**, mean **167.4148**
- `SM_100_200cm_mm`: min **237.2836**, max **437.3312**, mean **310.2233**
- `SM_0_40cm_mm`: min **53.4236**, max **159.0646**, mean **107.4657**
- `SM_0_100cm_mm`: min **142.4621**, max **401.3282**, mean **274.8805**
- `SM_0_200cm_mm`: min **386.8502**, max **837.8967**, mean **585.1037**
- `RootMoist_mm`: min **142.0403**, max **400.8547**, mean **274.4417**
- `surface_runoff_mm_day`: min **0.0000**, max **54.2026**, mean **0.4400**
- `baseflow_subsurface_mm_day`: min **0.0076**, max **50.8512**, mean **1.8909**
- `total_runoff_mm_day`: min **0.0078**, max **80.3488**, mean **2.3309**
- `GLDAS_ET_mm_day`: min **0.2504**, max **8.1495**, mean **2.6539**

## Negative-value scan

- `SM_0_10cm_mm`: negative values = **0**
- `SM_10_40cm_mm`: negative values = **0**
- `SM_40_100cm_mm`: negative values = **0**
- `SM_100_200cm_mm`: negative values = **0**
- `SM_0_40cm_mm`: negative values = **0**
- `SM_0_100cm_mm`: negative values = **0**
- `SM_0_200cm_mm`: negative values = **0**
- `RootMoist_mm`: negative values = **0**
- `surface_runoff_mm_day`: negative values = **0**
- `baseflow_subsurface_mm_day`: negative values = **0**
- `total_runoff_mm_day`: negative values = **0**
- `GLDAS_ET_mm_day`: negative values = **0**

## What I learned in GEE

- GLDAS variables must be aggregated according to their temporal semantics, not with one generic reducer.
- `_inst` variables are instantaneous states; daily representative values were calculated as the mean of sub-daily snapshots.
- `_acc` variables are accumulated amounts over the preceding 3-hour interval; daily values were calculated by summing the eight interval amounts.
- `_tavg` variables are mean rates over the preceding 3-hour interval; `Evap_tavg` was multiplied by 10,800 seconds for each interval and then summed.
- The flux day is shifted relative to timestamps: calendar day D uses timestamps from D 03:00 through D+1 00:00, implemented with `[D+03h, D+1+03h)`.
- Cumulative soil-moisture storage is the sum of physical layer storages, not the mean of layers.
- Temporal aggregation was completed before spatial averaging over AEZ-26.
- Chunked export was only a computational execution strategy; formulas, time windows, scale, AOI and reducers were identical in all five chunks.

## Methodology record

GLDAS v2.1 Noah 3-hourly data were converted to daily AEZ-26 time series using variable-specific temporal rules. Instantaneous soil-moisture and root-zone state variables were averaged across snapshots within each UTC day. Surface runoff (`Qs_acc`) and subsurface runoff/baseflow (`Qsb_acc`) were summed across the eight 3-hour accumulated intervals assigned to each calendar day. `Evap_tavg` was integrated by multiplying each 3-hour mean rate by 10,800 seconds and summing the resulting interval water depths. The flux window was shifted to `[D+03:00, D+1+03:00)` because `_acc` and `_tavg` describe the preceding 3-hour interval. Cumulative 0–40, 0–100 and 0–200 cm soil-water storages were formed by summing the corresponding physical layers. Daily rasters were then spatially averaged over the AEZ-26 geometry at approximately the native GLDAS 0.25° scale. The first study day contains seven state snapshots because the GLDAS-2.1 collection begins at 03:00 UTC; this was retained and QC-flagged rather than filled.