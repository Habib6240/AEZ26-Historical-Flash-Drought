# Phase 1E — MOD13Q1 NDVI/EVI: Final QC and Learning Notes

## Final status

**PASS — The 2000–2025 MOD13Q1 native 16-day vegetation-index dataset was exported and internally validated.**

## Dataset QC

- Rows / composites: **595**
- First composite: **2000-02-18**
- Last composite: **2025-12-19**
- Duplicate start dates: **0**
- Nominal temporal resolution: **16 days for all 595 rows**
- All-valid NDVI/EVI missing: **0**
- Standard-QA NDVI/EVI missing: **9 composites**
- Strict-QA NDVI/EVI missing: **151 composites**
- Standard-QA zero-coverage composites: **9**
- Strict-QA zero-coverage composites: **151**

The standard- and strict-QA missing counts exactly match their zero-coverage counts, so missing QA values were preserved as null rather than converted to zero.

## Timing note

MOD13Q1 starts in this Earth Engine series on **2000-02-18**. From 2001 onward there are 23 nominal 16-day composites per year; the 2000 record is partial because the MODIS Terra vegetation-index series does not begin on 2000-01-01. Year-boundary gaps are 13 or 14 days because the nominal MODIS 16-day schedule resets by day-of-year each calendar year; this is expected and was not interpolated.

## QA consistency

- `standard_QA_fraction = SummaryQA_good_fraction + SummaryQA_marginal_fraction` to numerical precision.
- `strict_QA_fraction <= standard_QA_fraction <= all_valid_fraction` for every composite.
- Standard and strict availability flags are fully consistent with whether coverage is greater than zero.

## Full-period ranges

- NDVI all-valid: **0.1360 to 0.8325**
- EVI all-valid: **0.0996 to 0.6424**
- NDVI standard-QA: **0.2976 to 0.8510**
- EVI standard-QA: **0.1631 to 0.6501**
- NDVI strict-QA: **0.2468 to 0.8584**
- EVI strict-QA: **0.1222 to 0.6620**

All exported regional means lie inside physically valid MOD13Q1 scaled ranges.

## Spatial-coverage summary

- Mean all-valid fraction: **0.9994**
- Mean standard-QA fraction: **0.7305**
- Median standard-QA fraction: **0.9671**
- Mean strict-QA fraction: **0.2808**
- Median strict-QA fraction: **0.0643**

The strict track is intentionally sparse and should be treated as a sensitivity/high-confidence track, not the primary vegetation series.

The standard-QA series is substantially more usable, but some composites—especially cloud-affected monsoon periods—have very low or zero accepted coverage. These coverage fields must be carried into later preprocessing and modeling.

## What I learned in GEE

- MOD13Q1 should be preserved at native 16-day timing rather than converted into synthetic daily observations during acquisition.
- Raw NDVI/EVI need the 0.0001 scale factor.
- `SummaryQA <= 1` provides a standard-quality vegetation track.
- DetailedQA bits allow a stricter high-confidence sensitivity track.
- Masked/invalid vegetation pixels are not equivalent to NDVI/EVI = 0.
- Spatial coverage fractions are essential metadata for deciding later whether to retain, flag, interpolate, or exclude low-coverage composites.
- All-valid, standard-QA and strict-QA tracks answer different methodological questions and should not be conflated.

## Methodology record

MOD13Q1 Collection 6.1 NDVI and EVI were processed at native 16-day composite timing over AEZ-26. Stored values were screened to the documented valid range and scaled by 0.0001. An all-valid diagnostic track retained physically valid source pixels; a standard-QA track retained SummaryQA classes 0 and 1; and a deliberately strict sensitivity track required good MODLAND VI quality, accepted usefulness codes, aerosol quantity <= 2, no adjacent or mixed cloud, land-only pixels, no snow/ice, and no shadow. Regional means and spatial QA fractions were exported for every native composite. Missing QA coverage was retained as null rather than filled.
