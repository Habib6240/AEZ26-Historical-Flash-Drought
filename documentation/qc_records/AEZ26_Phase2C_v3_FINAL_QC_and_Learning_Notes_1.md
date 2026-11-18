# AEZ-26 Phase 2C v3 — Final QC and Learning Notes

## Final status

**PASS — Phase 2C v3 is the authoritative flash-drought detection output for the current methodology.**

The uploaded ZIP was independently unpacked and all six generated CSV files were audited together. The v3 first-threshold-crossing correction is working as intended.

The earlier Phase 2C / Phase 2C v2 outputs and learning notes are **superseded** and should not be used as the final event catalogue.

---

## 1. Files audited

The ZIP contained exactly the expected six Phase 2C v3 outputs:

1. `AEZ26_Pentad_Hydroclimate_Indicators_2000_2025.csv`
2. `AEZ26_Flash_Drought_Event_Catalogue_Primary_2000_2025.csv`
3. `AEZ26_Flash_Drought_Event_Catalogue_Sensitivity_RootMoist_2000_2025.csv`
4. `AEZ26_Flash_Drought_Event_Catalogue_Sensitivity_Window5_2000_2025.csv`
5. `AEZ26_Flash_Drought_Event_Catalogue_Sensitivity_India25_Max18_2000_2025.csv`
6. `AEZ26_Phase2C_Flash_Drought_Detection_QC.csv`

---

## 2. Pentad-table QC

- Daily input rows represented: **9,497**
- Pentad rows: **1,898**
- Study years: **26**
- Pentads per year: **73 for every year**
- 5-day pentads: **1,891**
- 6-day leap-year pentads: **7**
- Other pentad lengths: **0**
- Duplicate `(year, pentad)` combinations: **0**
- Duplicate pentad labels: **0**
- Missing primary soil-moisture percentiles: **0**
- Missing RootMoist percentiles: **0**
- Missing ±2-pentad-window percentiles: **0**

The seven 6-day pentads occur in leap years 2000, 2004, 2008, 2012, 2016, 2020 and 2024, covering February 25 through March 1. This confirms that February 29 was retained without shifting subsequent climatological pentads.

Each climatological pentad contains exactly **26 annual reference values** for the primary same-pentad retrospective percentile calculation.

---

## 3. Final event counts

### Primary catalogue
**39 regional AEZ-26 flash-drought events**

### Sensitivity catalogues

- `RootMoist_mm` sensitivity: **39 events**
- ±2-pentad seasonal-window percentile sensitivity: **36 events**
- India-style 25th-percentile recovery + maximum 18 pentads: **35 events**

These event counts are outputs of the pre-specified methodology and were not tuned to obtain a preferred number of events.

---

## 4. Independent event-logic audit

Every primary event was independently reconstructed from the pentad table.

For all **39 primary events**:

- Pre-onset anchor percentile is **>40**: PASS
- Reported drought-threshold crossing is **<=20**: PASS
- Reported crossing is the **first <=20 crossing after the qualifying anchor**: PASS
- No new >40 anchor occurs between the selected anchor and crossing: PASS
- Mean intensification rate is **>=5 percentile points per pentad**: PASS
- Total event duration is **>=3 pentads**: PASS
- Onset is the first pentad after the qualifying >40 anchor: PASS
- Recovery threshold is satisfied correctly: PASS
- Reported intensification rate exactly matches recalculation: PASS
- Reported duration exactly matches recalculation: PASS
- Reported minimum percentile exactly matches recalculation: PASS
- Reported severity exactly matches recalculation: PASS
- Event overlaps: **0**
- Right-censored primary events: **0**

The primary event-phase flags and event IDs stored in the pentad table also match the reconstructed primary catalogue exactly.

---

## 5. Sensitivity-catalogue audit

The same first-crossing, intensification-rate, duration, recovery and non-overlap checks were applied to all three sensitivity catalogues.

- RootMoist sensitivity: **PASS**
- Seasonal-window sensitivity: **PASS**
- India-style sensitivity: **PASS**

The RootMoist sensitivity produced the **same 39 onset pentads** as the primary 0–100 cm soil-moisture catalogue. This is strong evidence that the identified regional onset chronology is robust to the choice between the two closely related GLDAS root-zone soil-water variables.

The ±2-pentad seasonal-window sensitivity shares **25 exact onset pentads** with the primary catalogue and contains 36 events overall. This larger difference is scientifically useful rather than an error: it shows that event identification is more sensitive to the percentile-climatology formulation than to the GLDAS root-zone variable choice. This sensitivity must be retained and discussed later.

The India-style catalogue contains **35 events** and shares **34 exact onset pentads** with the primary catalogue. The difference mainly reflects the alternative 25th-percentile recovery and maximum-duration treatment.

---

## 6. Primary-event characteristics

Across the 39 primary events:

- Total duration: **3 to 58 pentads**
- Median total duration: **5 pentads**
- Intensification duration: **1 to 8 pentads**
- Median intensification duration: **2 pentads**
- Mean intensification rate: **5.77 to 53.85 percentile points per pentad**
- Median intensification rate: **14.10 percentile points per pentad**
- Severity (40th-percentile deficit metric): **31.54 to 1958.46 percentile-point pentads**
- Events flagged as prolonged after flash onset (`>18` pentads): **4**

The four prolonged events are retained in the primary catalogue because rapid onset and subsequent drought persistence are stored as separate concepts. They should receive explicit sensitivity treatment during Phase 2D and should not be described as being in continuous “flash intensification” throughout their full duration.

---

## 7. What changed from the superseded versions

### Superseded early version
An unsupported hard maximum of four pentad transitions was initially imposed.

### Superseded v2
That hard cap was removed, but six events reused an old >40 anchor across an intervening dry excursion/recovery.

### Final v3
The detector now evaluates the **first <=20th-percentile crossing after a >40 anchor**. If the first dry excursion does not satisfy the flash-drought criteria, it is rejected and the detector resumes after recovery. The old anchor is never bridged across a recovered excursion.

The resulting final primary event count is **39**, not 40 or 45.

---

## 8. Interpretation boundary

The current Phase-1 data workflow exported an **AEZ-26 regional-mean soil-moisture time series**.

Therefore, these 39 events represent:

**regional AEZ-26 flash-drought episodes**

They do **not** represent:
- grid-cell flash-drought frequency,
- percentage of AEZ land under flash drought,
- spatial flash-drought extent, or
- subregional onset timing.

Any future spatial claim would require a spatial/grid-level workflow rather than the current regional-mean time series.

---

## 9. Methodological safeguards retained

- The raw Phase 2A daily backbone remains unchanged.
- MOD13, MOD16, GRACE and JRC were not used to define the flash-drought label.
- Atmospheric drivers were not used to tune the primary event label.
- Missing values were not converted to zero.
- No random train/test split has been created.
- No whole-record ML scaling has been performed.
- Climate extremes were not deleted as generic outliers.
- Sensitivity results were retained instead of being adjusted to agree with the primary catalogue.

---

## 10. What I learned in Google Colab / Python

- A ZIP containing an entire output folder is convenient for reproducible audit because related CSVs can be inspected together.
- Structural QC is not enough; an event catalogue must be independently reconstructed from the underlying indicator table.
- Sequential event-detection algorithms require explicit state transitions so that an old onset anchor cannot be reused after recovery.
- `validate`, assertions and independent post-run audits are complementary safeguards.
- Sensitivity analyses can reveal which methodological choices materially affect the inventory.
- A matching event count does not prove a correct algorithm; event-by-event chronology must also be checked.
- Derived research products should be versioned when methodology changes rather than silently overwriting the interpretation of older outputs.

---

## 11. Phase 2C final gate

**Phase 2C v3: FINAL PASS**

Authoritative current outputs:

- Primary regional flash-drought catalogue: **39 events**
- RootMoist sensitivity: **39**
- Seasonal-window sensitivity: **36**
- India-style sensitivity: **35**

The project may now proceed to **Phase 2D — event verification, seasonal climatology and compound-driver characterization** without changing the locked primary event labels.
