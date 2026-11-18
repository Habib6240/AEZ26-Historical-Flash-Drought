# Phase 1B — ERA5-Land: QC and Learning Notes

## Final status

**PASS — The five ERA5-Land chunks were merged into one complete daily 2000–2025 dataset.**

## Assembly and QC

- Rows: **9497**
- Date range: **2000-01-01 to 2025-12-31**
- Missing calendar dates: **0**
- Duplicate dates: **0**
- Total missing cells: **0**
- Days with hourly image count != 24: **0**
- Days with daily-aggregate image count != 1: **0**
- Days with incomplete flag: **0**
- Tmax ≥ Tmean ≥ Tmin violations: **0**
- RH outside 0–100%: **0**
- Negative VPD mean: **0**
- VPDmax < VPDmean: **0**
- Negative wind speed: **0**
- Negative incoming solar radiation: **0**
- Maximum radiation identity error: **1.243e-14 MJ/m²/day**

## Selected full-period ranges

- `t2m_mean_C`: min **12.2622**, max **35.9553**, mean **25.1868**
- `t2m_max_C`: min **15.6285**, max **42.6972**, mean **29.8124**
- `t2m_min_C`: min **6.5536**, max **30.8475**, mean **20.9822**
- `relative_humidity_mean_pct`: min **21.9466**, max **98.3278**, mean **74.2883**
- `VPD_mean_kPa`: min **0.0489**, max **4.2625**, mean **0.9189**
- `VPD_max_kPa`: min **0.0985**, max **7.5375**, mean **1.9333**
- `wind_speed_mean_m_s`: min **0.5971**, max **7.3213**, mean **1.9575**
- `solar_radiation_MJ_m2_day`: min **1.1229**, max **28.7070**, mean **16.7173**
- `net_radiation_MJ_m2_day`: min **-1.1566**, max **16.3871**, mean **8.8680**
- `total_evaporation_mm_day`: min **0.2906**, max **5.2329**, mean **2.4067**
- `ERA5_potential_evaporation_mm_day`: min **0.6743**, max **20.2237**, mean **6.3482**

## What I learned in GEE

- ERA5-Land Hourly and Daily Aggregated collections serve different methodological roles.
- Hourly RH, VPD, and wind magnitude are derived before daily aggregation.
- Temporal aggregation and spatial aggregation are separate operations.
- `mean(hourly VPD)` is not equivalent to VPD computed from daily mean temperature/dewpoint.
- Hourly wind magnitude is calculated as `sqrt(u²+v²)` before daily averaging.
- ERA5 units were explicitly converted: Kelvin→°C, J/m²→MJ/m², and evaporation m water equivalent→positive mm/day.
- ERA5 potential evaporation is kept distinct from FAO-56 reference ET₀.
- The five date chunks were only a memory-safe export strategy; the scientific method was unchanged across chunks.

## Methodology record

For each UTC calendar day, ERA5-Land hourly 2 m temperature and dewpoint were converted from Kelvin to Celsius. Hourly saturation and actual vapor pressure were calculated, followed by hourly relative humidity and vapor pressure deficit. Hourly 10 m wind magnitude was calculated from the u and v components. These hourly variables were temporally aggregated to daily mean values, with daily maximum VPD retained separately. Daily maximum/minimum temperature, radiation accumulations, total evaporation and potential evaporation were obtained from the ERA5-Land Daily Aggregated collection with explicit unit/sign conversion. The daily rasters were then spatially averaged over the AEZ-26 study geometry at approximately the native ERA5-Land grid scale.