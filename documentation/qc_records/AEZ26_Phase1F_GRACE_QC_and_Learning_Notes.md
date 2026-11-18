# Phase 1F — GRACE / GRACE-FO JPL Mascon: Final QC and Learning Notes

## Final status

**PASS — The native-timing GRACE/GRACE-FO JPL RL06.3Mv04 CRI-filtered mascon time series was exported and internally validated.**

## Dataset QC

- Rows / native observations: **238**
- First native observation: **2002-04-03**
- First native end date: **2002-04-29**
- Last native observation: **2024-09-30**
- Last native end date: **2024-10-30**
- Duplicate native dates: **0**
- Duplicate timestamps: **0**
- Missing TWSA values: **0**
- Missing uncertainty values: **0**
- Availability flags: **{1: 238}**
- `system:index` start date matches exported native date for every row: **True**
- `system:index` end date matches exported native end date for every row: **True**

## 2020 validation

- Native date: **2020-01-31**
- TWSA: **-12.5406 cm**
- Mean mascon uncertainty: **3.7867 cm**

This matches the earlier diagnostic calculation.

## Full-period ranges

- Regional TWSA: **-40.7215 to 41.0306 cm**
- Mean regional TWSA across native observations: **-6.4241 cm**
- Mean mascon uncertainty: **2.8848 to 22.8878 cm**
- Mean of the uncertainty column: **4.4047 cm**

The large uncertainty values at some mission-edge observations are retained rather than deleted automatically.

## Native timing and gaps

GRACE/GRACE-FO was **not** forced onto a regular monthly calendar. Native observation intervals and mission gaps were preserved.

- Largest start-to-start gap in this exported series: **374 days**
- Gap spans from the observation starting **2017-05-22** to the next observation starting **2018-05-31**

This long gap corresponds to the GRACE-to-GRACE-FO mission transition and is not filled in GEE.

## Important scientific interpretation

- `TWSA_cm` is **terrestrial water-storage anomaly**, not groundwater storage alone.
- Groundwater interpretation later requires accounting for other terrestrial-water-storage components and, ideally, independent groundwater-well observations.
- `mean_mascon_uncertainty_cm` is the spatial mean of provider 1-sigma mascon uncertainty values over AEZ-26. It is **not** a formal propagated uncertainty of the AEZ regional mean.
- The Earth Engine grid is a convenient gridded representation. Adjacent output cells should not be treated as independent ~0.5° observations because the independent mascon information is much coarser.

## What I learned in GEE

- Native satellite observation timing can be irregular and should not automatically be converted to a regular monthly sequence.
- `system:index`, `system:time_start`, and `system:time_end` are useful for preserving traceability to native observations.
- Regional raster reduction and uncertainty interpretation are different issues: spatially averaging an uncertainty band does not create a statistically propagated regional uncertainty.
- Missing mission periods are scientific missingness, not zeros.
- GRACE TWSA should not be relabeled as groundwater without a defensible component-separation methodology.

## Methodology record

The JPL RL06.3Mv04 CRI-filtered GRACE/GRACE-FO mascon product was sampled over the AEZ-26 study geometry at the Earth Engine grid scale. For each native observation, regional mean liquid-water-equivalent thickness (`lwe_thickness`) and regional mean provider uncertainty were exported together with the native system index, start timestamp and end date. Native irregular timing and mission gaps were retained without interpolation. The resulting `TWSA_cm` field is treated as terrestrial water-storage anomaly and is not interpreted as groundwater storage by itself.
