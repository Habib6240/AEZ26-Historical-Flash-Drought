# Phase 1G — JRC Monthly Surface Water: Final QC and Learning Notes

## Final status

**PASS — The complete JRC Monthly History series for AEZ-26 from 2000-01 through 2021-12 was exported and internally validated.**

## Dataset QC

- Final rows / months: **264**
- Date range: **2000-01-01 to 2021-12-01**
- Missing calendar months: **0**
- Duplicate months: **0**
- Months with missing water area: **13**
- Months with missing valid-observation fraction: **0**
- JRC rasterized reference area: **1542.2443 to 1542.2443 km²**
- Valid-observation fraction: **0.000000 to 1.000000**
- Mean valid-observation fraction: **0.758463**
- Median valid-observation fraction: **0.934682**
- Low-coverage months (<70%): **79**
- Months with no valid observations: **13**
- Months with detected surface water: **251**

## Internal consistency

- Maximum exported area-balance error: **5.684e-12 km²**
- Maximum independently recomputed `water + non-water - valid area` error: **5.684e-12 km²**
- Maximum `water fraction + non-water fraction - 1` error: **3.553e-15**
- `no_valid_observation_flag` mismatches: **0**
- `low_coverage_flag` mismatches: **0**
- `water_detected_flag` mismatches: **0**

## July 2020 validation

- Reference raster area: **1542.2443 km²**
- Valid observed area: **8.7223 km²**
- Valid-observation fraction: **0.005656**
- Water area: **4.0966 km²**
- Water fraction of valid area: **0.469673**
- Low-coverage flag: **1**

This confirms the earlier diagnostic: July 2020 had very low valid Landsat/JRC coverage, so its observed water area must not be interpreted as a complete AEZ-wide water extent.

## Full-period surface-water range

- Observed water area: **0.0016 to 30.8556 km²**
- Mean observed water area across months with valid observations: **7.9115 km²**

These values describe **observed surface-water area**, not storage volume.

## What I learned in GEE

- JRC Monthly History stores categorical water classes rather than a continuous hydrological variable.
- Class 0 means **no data**, class 1 means valid non-water, and class 2 means valid water.
- No-data pixels must not be converted into zero-water observations.
- `ee.Image.pixelArea()` is used to convert classified pixels into physical area.
- Valid observed area and detected water area are different quantities and must be exported together.
- A month with valid observations but no detected water should have water area = 0.
- A month with no valid observations should have water area = null, not zero.
- Spatial coverage fraction is essential for interpreting monthly water area.
- A QC threshold can flag low-coverage months without automatically deleting them.
- Surface-water **area (km²)** is not surface-water **storage volume**, so it cannot be directly subtracted from GRACE TWSA in cm.

## Methodology record

JRC Global Surface Water Monthly History v1.4 was processed at its native monthly timing for 2000–2021. Within AEZ-26, class 1 and class 2 pixels were treated as valid observations, while class 0 was treated as no data. Pixel area was summed separately for valid observations, detected water, and valid non-water. Monthly water area was reported only when valid observations existed; otherwise it remained null. Valid-observation fraction and a <70% low-coverage flag were retained as QC metadata. Water and non-water area balances were independently checked and found numerically consistent.
