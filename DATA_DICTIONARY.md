# Data dictionary (files of the derived-dataset record)

This dictionary describes the files in the Zenodo **derived-dataset record**; it is shipped with both records. The software release does not contain these files. Column names are read from the file headers; meanings follow the manuscript Methods and the scripts that produced the files. Units: soil water in mm (0–100 cm), precipitation and evapotranspiration in mm per pentad, VPD in kPa, temperature in °C, z = standardised anomaly, p_perm = Monte Carlo permutation p-value, q = Benjamini–Hochberg-adjusted p. A pentad is one of 73 climatological five-day periods per year (leap years: P12 has six days and later pentads shift by one day).

Integrity notes
- `data/pentad_indicators/AEZ26_Pentad_Hydroclimate_Indicators_2000_2025.csv` is **file A, canonical** (Phase 2C v3, 39-event annotation; SHA-256 `44f76cbf8a66758087ffb5b708e5897a1f3c86a4f4726f6f66b5dbea64dfe9b3`). `historical_inputs/phase7a_locked_input/` holds **file B** (legacy 40-event annotation; SHA-256 `588e505b9d33769f9146c289e75edda1948eb80e00d57b100b9f1776fc72e4b4`), the table locked by the original Phase 7A notebook. B is not the canonical table. They differ only in `primary_flash_drought_event_flag`, `_event_id`, `_intensification_flag` and `_drought_phase_flag`.
- `data/phase7a_chunks_sanitized/` are the nine Phase 7A export chunks in which the private Earth Engine asset identifier is replaced by `projects/<YOUR-EE-PROJECT>/assets/<YOUR-AEZ26-ASSET>`; their hashes differ from the originals and `data/phase7a_chunks_sanitized/CHUNK_HASH_MAP.csv` maps each. Raw chunks are not released.
- `data/event_catalogue/AEZ26_Phase7A_GLDAS_Primary_Candidate_Audit.csv` is the stored three-row audit. Only the 39-row catalogue copy is available; the other two (40 and 45 rows, SHA-256 `69c8dc0c…` and `db6e218b…`) could not be supplied, so a re-run reproduces the audit only in part.
- Numerical values are those of the author's runs; the only edit to any data file is the placeholder replacement above.


## `data/chronology_comparison/AEZ26_Phase2G_Robustness_Sensitivity.csv`
Statistical association tables, robustness and cohort summaries
Rows: 33. Columns (10): `analysis_type`, `variant`, `predictor`, `predictor_label`, `outcome`, `n`, `rho`, `ci_low`, `ci_high`, `median_response_depth_z`

## `data/chronology_comparison/AEZ26_Phase7A_Method_Config.txt`

Text/JSON/Markdown file.

## `data/chronology_comparison/AEZ26_Robustness_Continuous_State_Agreement.csv`
Continuous-state agreement between sources
Rows: 2. Columns (3): `metric`, `value`, `p_value`

## `data/chronology_comparison/AEZ26_Robustness_ERA5Land_Long45_Event_Catalogue_1981_2025.csv`
ERA5-Land 45-year (LONG45) event catalogue
Rows: 74. Columns (25): `catalogue`, `event_id`, `anchor_pentad`, `anchor_percentile`, `onset_pentad`, `onset_start_date`, `onset_mid_date`, `threshold_crossing_pentad`, `threshold_crossing_percentile`, `event_end_pentad`, `recovery_pentad`, `right_censored_flag`, `intensification_duration_pentads`, `total_duration_pentads`, `total_duration_actual_days`, `mean_intensification_rate_pp_per_pentad`, `minimum_soil_moisture_percentile`, `severity_40pct_deficit_pp_pentads`, `onset_year`, `onset_month`, `antecedent_4pentad_precipitation_mm`, `event_precipitation_mm`, `event_VPD_mean_kPa`, `event_t2m_mean_C`, `event_ERA5_potential_evaporation_mm`

## `data/chronology_comparison/AEZ26_Robustness_ERA5Land_Source26_Event_Catalogue_2000_2025.csv`
ERA5-Land 2000–2025 (OVERLAP26) event catalogue
Rows: 44. Columns (25): `catalogue`, `event_id`, `anchor_pentad`, `anchor_percentile`, `onset_pentad`, `onset_start_date`, `onset_mid_date`, `threshold_crossing_pentad`, `threshold_crossing_percentile`, `event_end_pentad`, `recovery_pentad`, `right_censored_flag`, `intensification_duration_pentads`, `total_duration_pentads`, `total_duration_actual_days`, `mean_intensification_rate_pp_per_pentad`, `minimum_soil_moisture_percentile`, `severity_40pct_deficit_pp_pentads`, `onset_year`, `onset_month`, `antecedent_4pentad_precipitation_mm`, `event_precipitation_mm`, `event_VPD_mean_kPa`, `event_t2m_mean_C`, `event_ERA5_potential_evaporation_mm`

## `data/chronology_comparison/AEZ26_Robustness_Environment_and_Hashes.json`

Text/JSON/Markdown file.

## `data/chronology_comparison/AEZ26_Robustness_Event_Onset_Agreement.csv`
GLDAS–ERA5-Land onset agreement
Rows: 6. Columns (6): `comparison`, `tolerance_pentads`, `matched_primary_events`, `primary_total`, `sensitivity_total`, `primary_match_fraction`

## `data/chronology_comparison/AEZ26_Robustness_Long45_Period_Event_Rates.csv`
Long-record event rates/seasonality
Rows: 3. Columns (4): `period`, `events`, `years`, `events_per_year`

## `data/chronology_comparison/AEZ26_Robustness_Long45_Seasonality.csv`
Long-record event rates/seasonality
Rows: 4. Columns (2): `season`, `events`

## `data/chronology_comparison/AEZ26_Robustness_Long_Record_Trend_Diagnostics.csv`
Long-record trend diagnostics
Rows: 5. Columns (7): `metric`, `theil_sen_change_per_decade`, `theil_sen_95ci_low_per_decade`, `theil_sen_95ci_high_per_decade`, `kendall_tau`, `kendall_p_value`, `unit`

## `data/chronology_comparison/AEZ26_Robustness_QC.csv`
Phase 7A quality-control checks
Rows: 8. Columns (4): `check`, `value`, `expected`, `status`

## `data/environmental_drivers/AEZ26_Phase2D_Annual_Event_Counts_2000_2025.csv`

Rows: 26. Columns (2): `onset_year`, `event_count`

## `data/environmental_drivers/AEZ26_Phase2D_Driver_Class_Percentile_Sensitivity.csv`

Rows: 4. Columns (3): `percentile20_80_driver_class_sensitivity`, `event_count`, `event_percent`

## `data/environmental_drivers/AEZ26_Phase2D_Driver_Class_Summary.csv`
Event driver characterisation (precipitation and atmospheric-demand conditions)
Rows: 4. Columns (3): `primary_driver_class`, `event_count`, `event_percent`

## `data/environmental_drivers/AEZ26_Phase2D_Event_Driver_Characterization.csv`
Event driver characterisation (precipitation and atmospheric-demand conditions)
Rows: 39. Columns (49): `event_id`, `onset_pentad`, `onset_mid_date`, `onset_year`, `onset_month`, `onset_season`, `threshold_crossing_pentad`, `intensification_duration_pentads`, `intensification_actual_days`, `total_duration_pentads`, `severity_40pct_deficit_pp_pentads`, `mean_intensification_rate_pp_per_pentad`, `prolonged_after_flash_flag`, `seasonal_reference_window_count`, `intensification_precipitation_mm`, `intensification_PE_mm`, `intensification_VPD_mean_kPa`, `intensification_t2m_mean_C`, `intensification_net_radiation_mean_MJ_m2_day`, `intensification_wind_mean_m_s`, `intensification_RH_mean_pct`, `P_reference_mean_mm`, `P_reference_sd_mm`, `PE_reference_mean_mm`, `PE_reference_sd_mm`, `P_standardized_anomaly_z`, `PE_standardized_anomaly_z`, `VPD_standardized_anomaly_z`, `temperature_standardized_anomaly_z`, `net_radiation_standardized_anomaly_z`, `wind_standardized_anomaly_z`, `RH_standardized_anomaly_z`, `P_empirical_percentile`, `PE_empirical_percentile`, `VPD_empirical_percentile`, `temperature_empirical_percentile`, `net_radiation_empirical_percentile`, `wind_empirical_percentile`, `RH_empirical_percentile`, `large_precipitation_deficit_flag` …

## `data/environmental_drivers/AEZ26_Phase2D_Monthly_Onset_Summary.csv`

Rows: 12. Columns (4): `onset_month`, `event_count`, `month_name`, `event_percent`

## `data/environmental_drivers/AEZ26_Phase2D_Prolonged_Event_Diagnostics.csv`

Rows: 4. Columns (49): `event_id`, `onset_pentad`, `onset_mid_date`, `onset_year`, `onset_month`, `onset_season`, `threshold_crossing_pentad`, `intensification_duration_pentads`, `intensification_actual_days`, `total_duration_pentads`, `severity_40pct_deficit_pp_pentads`, `mean_intensification_rate_pp_per_pentad`, `prolonged_after_flash_flag`, `seasonal_reference_window_count`, `intensification_precipitation_mm`, `intensification_PE_mm`, `intensification_VPD_mean_kPa`, `intensification_t2m_mean_C`, `intensification_net_radiation_mean_MJ_m2_day`, `intensification_wind_mean_m_s`, `intensification_RH_mean_pct`, `P_reference_mean_mm`, `P_reference_sd_mm`, `PE_reference_mean_mm`, `PE_reference_sd_mm`, `P_standardized_anomaly_z`, `PE_standardized_anomaly_z`, `VPD_standardized_anomaly_z`, `temperature_standardized_anomaly_z`, `net_radiation_standardized_anomaly_z`, `wind_standardized_anomaly_z`, `RH_standardized_anomaly_z`, `P_empirical_percentile`, `PE_empirical_percentile`, `VPD_empirical_percentile`, `temperature_empirical_percentile`, `net_radiation_empirical_percentile`, `wind_empirical_percentile`, `RH_empirical_percentile`, `large_precipitation_deficit_flag` …

## `data/environmental_drivers/AEZ26_Phase2D_QC.csv`
Event driver characterisation (precipitation and atmospheric-demand conditions)
Rows: 11. Columns (4): `check`, `value`, `status`, `note`

## `data/environmental_drivers/AEZ26_Phase2D_Seasonal_Onset_Summary.csv`
Event driver characterisation (precipitation and atmospheric-demand conditions)
Rows: 4. Columns (3): `onset_season`, `event_count`, `event_percent`

## `data/environmental_drivers/AEZ26_Phase2D_Sensitivity_Agreement.csv`

Rows: 3. Columns (9): `sensitivity_catalogue`, `primary_event_count`, `sensitivity_event_count`, `exact_onset_matches`, `exact_match_percent_of_primary`, `within_1_pentad_matches`, `within_1_pentad_percent_of_primary`, `within_2_pentad_matches`, `within_2_pentad_percent_of_primary`

## `data/eq6_eq7_verification/eq6/eq6_chunk_sha256.csv`
See folder description.
Rows: 9. Columns (2): `file`, `sha256`

## `data/eq6_eq7_verification/eq6/eq6_pentad_comparison.csv`
See folder description.
Rows: 3285. Columns (5): `year`, `pentad_of_year`, `rec_mm`, `stored_mm`, `diff`

## `data/eq6_eq7_verification/eq6/eq6_reproduction_summary.json`

Text/JSON/Markdown file.

## `data/eq6_eq7_verification/eq6/layer_chunks/AEZ26_Phase7A_ERA5Land_Layers_Pentad_1981_1985.csv`
See folder description.
Rows: 365. Columns (10): `year`, `pentad_of_year`, `pentad_label`, `pentad_start`, `pentad_end`, `n_days`, `era5_daily_images`, `swvl1_mean_m3m3`, `swvl2_mean_m3m3`, `swvl3_mean_m3m3`

## `data/eq6_eq7_verification/eq6/layer_chunks/AEZ26_Phase7A_ERA5Land_Layers_Pentad_1986_1990.csv`
See folder description.
Rows: 365. Columns (10): `year`, `pentad_of_year`, `pentad_label`, `pentad_start`, `pentad_end`, `n_days`, `era5_daily_images`, `swvl1_mean_m3m3`, `swvl2_mean_m3m3`, `swvl3_mean_m3m3`

## `data/eq6_eq7_verification/eq6/layer_chunks/AEZ26_Phase7A_ERA5Land_Layers_Pentad_1991_1995.csv`
See folder description.
Rows: 365. Columns (10): `year`, `pentad_of_year`, `pentad_label`, `pentad_start`, `pentad_end`, `n_days`, `era5_daily_images`, `swvl1_mean_m3m3`, `swvl2_mean_m3m3`, `swvl3_mean_m3m3`

## `data/eq6_eq7_verification/eq6/layer_chunks/AEZ26_Phase7A_ERA5Land_Layers_Pentad_1996_2000.csv`
See folder description.
Rows: 365. Columns (10): `year`, `pentad_of_year`, `pentad_label`, `pentad_start`, `pentad_end`, `n_days`, `era5_daily_images`, `swvl1_mean_m3m3`, `swvl2_mean_m3m3`, `swvl3_mean_m3m3`

## `data/eq6_eq7_verification/eq6/layer_chunks/AEZ26_Phase7A_ERA5Land_Layers_Pentad_2001_2005.csv`
See folder description.
Rows: 365. Columns (10): `year`, `pentad_of_year`, `pentad_label`, `pentad_start`, `pentad_end`, `n_days`, `era5_daily_images`, `swvl1_mean_m3m3`, `swvl2_mean_m3m3`, `swvl3_mean_m3m3`

## `data/eq6_eq7_verification/eq6/layer_chunks/AEZ26_Phase7A_ERA5Land_Layers_Pentad_2006_2010.csv`
See folder description.
Rows: 365. Columns (10): `year`, `pentad_of_year`, `pentad_label`, `pentad_start`, `pentad_end`, `n_days`, `era5_daily_images`, `swvl1_mean_m3m3`, `swvl2_mean_m3m3`, `swvl3_mean_m3m3`

## `data/eq6_eq7_verification/eq6/layer_chunks/AEZ26_Phase7A_ERA5Land_Layers_Pentad_2011_2015.csv`
See folder description.
Rows: 365. Columns (10): `year`, `pentad_of_year`, `pentad_label`, `pentad_start`, `pentad_end`, `n_days`, `era5_daily_images`, `swvl1_mean_m3m3`, `swvl2_mean_m3m3`, `swvl3_mean_m3m3`

## `data/eq6_eq7_verification/eq6/layer_chunks/AEZ26_Phase7A_ERA5Land_Layers_Pentad_2016_2020.csv`
See folder description.
Rows: 365. Columns (10): `year`, `pentad_of_year`, `pentad_label`, `pentad_start`, `pentad_end`, `n_days`, `era5_daily_images`, `swvl1_mean_m3m3`, `swvl2_mean_m3m3`, `swvl3_mean_m3m3`

## `data/eq6_eq7_verification/eq6/layer_chunks/AEZ26_Phase7A_ERA5Land_Layers_Pentad_2021_2025.csv`
See folder description.
Rows: 365. Columns (10): `year`, `pentad_of_year`, `pentad_label`, `pentad_start`, `pentad_end`, `n_days`, `era5_daily_images`, `swvl1_mean_m3m3`, `swvl2_mean_m3m3`, `swvl3_mean_m3m3`

## `data/eq6_eq7_verification/eq7/AEZ26_Eq7_Temporal_Robustness_23pentads_v02.csv`
See folder description.
Rows: 23. Columns (31): `year`, `pentad_of_year`, `stratum`, `pentad_start`, `pentad_end`, `n_days`, `era5_images`, `A_t2m_C`, `A_td_C`, `A_RH_pct`, `A_VPD_mean_kPa`, `A_VPD_max_kPa`, `A_SM_0_100_mm`, `A_n_sum`, `A_n_count`, `B_t2m_C`, `B_td_C`, `B_RH_pct`, `B_VPD_mean_kPa`, `B_VPD_max_kPa`, `B_SM_0_100_mm`, `B_n_sum`, `B_n_count`, `C_t2m_C`, `C_td_C`, `C_RH_pct`, `C_VPD_mean_kPa`, `C_VPD_max_kPa`, `C_SM_0_100_mm`, `C_n_sum`, `C_n_count`

## `data/eq6_eq7_verification/eq7/BA_overall.csv`
See folder description.
Rows: 6. Columns (8): ``, `bias`, `MAE`, `RMSE`, `max`, `sd`, `min`, `maxv`

## `data/eq6_eq7_verification/eq7/era5_baseline.json`

Text/JSON/Markdown file.

## `data/eq6_eq7_verification/eq7/era5_catalogue_mc.json`

Text/JSON/Markdown file.

## `data/eq6_eq7_verification/eq7/flag_margins.csv`
See folder description.
Rows: 3. Columns (6): `var`, `n_flagged`, `min_margin`, `n_within_0p05`, `n_within_0p10`, `n_within_0p25`

## `data/eq6_eq7_verification/eq7/flag_montecarlo_measured_sd.csv`
See folder description.
Rows: 9. Columns (5): `noise_scale`, `var`, `expected_flips_per_run`, `events_flipping_ge5pct_runs`, `max_abs_dz`

## `data/eq6_eq7_verification/eq7/pentad_comparison_23.csv`
See folder description.
Rows: 23. Columns (42): `year`, `pentad_of_year`, `stratum`, `pentad_start`, `pentad_end`, `n_days`, `era5_images`, `A_t2m_C`, `A_td_C`, `A_RH_pct`, `A_VPD_mean_kPa`, `A_VPD_max_kPa`, `A_SM_0_100_mm`, `A_n_sum`, `A_n_count`, `B_t2m_C`, `B_td_C`, `B_RH_pct`, `B_VPD_mean_kPa`, `B_VPD_max_kPa`, `B_SM_0_100_mm`, `B_n_sum`, `B_n_count`, `C_t2m_C`, `C_td_C`, `C_RH_pct`, `C_VPD_mean_kPa`, `C_VPD_max_kPa`, `C_SM_0_100_mm`, `C_n_sum`, `C_n_count`, `t2m_mean_C`, `relative_humidity_mean_pct`, `VPD_mean_kPa`, `VPD_dailymean_max_kPa`, `ERA5_SM_0_100_mean_mm`, `d_t2m_C`, `d_td_C`, `d_RH_pct`, `d_VPD_mean_kPa` …

## `data/eq6_eq7_verification/eq7/pooled_year_to_year_sd.csv`
See folder description.
Rows: 6. Columns (2): ``, `sd`

## `data/eq6_eq7_verification/eq7/trend_drift_sensitivity.csv`
See folder description.
Rows: 122. Columns (9): `var`, `drift_per_decade`, `slope_per_decade`, `ci_lo`, `ci_hi`, `nominal_p`, `BH_q`, `CI_excludes_0`, `FDR_supported`

## `data/event_catalogue/AEZ26_Flash_Drought_Event_Catalogue_Primary_2000_2025.csv`
Primary 39-event GLDAS 0–100 cm flash-drought catalogue (locked)
Rows: 39. Columns (35): `catalogue`, `event_id`, `anchor_pentad`, `anchor_mid_date`, `anchor_percentile`, `onset_pentad`, `onset_start_date`, `onset_mid_date`, `threshold_crossing_pentad`, `threshold_crossing_mid_date`, `threshold_crossing_percentile`, `event_end_pentad`, `event_end_date`, `recovery_pentad`, `termination_mid_date`, `recovery_threshold_percentile`, `right_censored_flag`, `intensification_duration_pentads`, `total_duration_pentads`, `total_duration_actual_days`, `mean_intensification_rate_pp_per_pentad`, `minimum_soil_moisture_percentile`, `severity_40pct_deficit_pp_pentads`, `prolonged_after_flash_flag`, `onset_year`, `onset_month`, `antecedent_4pentad_precipitation_mm`, `antecedent_4pentad_VPD_mean_kPa`, `event_precipitation_mm`, `event_VPD_mean_kPa`, `event_VPD_max_kPa`, `event_t2m_mean_C`, `event_t2m_max_C`, `event_ERA5_potential_evaporation_mm`, `event_GLDAS_ET_mm`

## `data/event_catalogue/AEZ26_Flash_Drought_Event_Catalogue_Sensitivity_India25_Max18_2000_2025.csv`
Detector-sensitivity catalogue (alternative window/threshold/soil-moisture definition)
Rows: 35. Columns (35): `catalogue`, `event_id`, `anchor_pentad`, `anchor_mid_date`, `anchor_percentile`, `onset_pentad`, `onset_start_date`, `onset_mid_date`, `threshold_crossing_pentad`, `threshold_crossing_mid_date`, `threshold_crossing_percentile`, `event_end_pentad`, `event_end_date`, `recovery_pentad`, `termination_mid_date`, `recovery_threshold_percentile`, `right_censored_flag`, `intensification_duration_pentads`, `total_duration_pentads`, `total_duration_actual_days`, `mean_intensification_rate_pp_per_pentad`, `minimum_soil_moisture_percentile`, `severity_40pct_deficit_pp_pentads`, `prolonged_after_flash_flag`, `onset_year`, `onset_month`, `antecedent_4pentad_precipitation_mm`, `antecedent_4pentad_VPD_mean_kPa`, `event_precipitation_mm`, `event_VPD_mean_kPa`, `event_VPD_max_kPa`, `event_t2m_mean_C`, `event_t2m_max_C`, `event_ERA5_potential_evaporation_mm`, `event_GLDAS_ET_mm`

## `data/event_catalogue/AEZ26_Flash_Drought_Event_Catalogue_Sensitivity_RootMoist_2000_2025.csv`
Detector-sensitivity catalogue (alternative window/threshold/soil-moisture definition)
Rows: 39. Columns (35): `catalogue`, `event_id`, `anchor_pentad`, `anchor_mid_date`, `anchor_percentile`, `onset_pentad`, `onset_start_date`, `onset_mid_date`, `threshold_crossing_pentad`, `threshold_crossing_mid_date`, `threshold_crossing_percentile`, `event_end_pentad`, `event_end_date`, `recovery_pentad`, `termination_mid_date`, `recovery_threshold_percentile`, `right_censored_flag`, `intensification_duration_pentads`, `total_duration_pentads`, `total_duration_actual_days`, `mean_intensification_rate_pp_per_pentad`, `minimum_soil_moisture_percentile`, `severity_40pct_deficit_pp_pentads`, `prolonged_after_flash_flag`, `onset_year`, `onset_month`, `antecedent_4pentad_precipitation_mm`, `antecedent_4pentad_VPD_mean_kPa`, `event_precipitation_mm`, `event_VPD_mean_kPa`, `event_VPD_max_kPa`, `event_t2m_mean_C`, `event_t2m_max_C`, `event_ERA5_potential_evaporation_mm`, `event_GLDAS_ET_mm`

## `data/event_catalogue/AEZ26_Flash_Drought_Event_Catalogue_Sensitivity_Window5_2000_2025.csv`
Detector-sensitivity catalogue (alternative window/threshold/soil-moisture definition)
Rows: 36. Columns (35): `catalogue`, `event_id`, `anchor_pentad`, `anchor_mid_date`, `anchor_percentile`, `onset_pentad`, `onset_start_date`, `onset_mid_date`, `threshold_crossing_pentad`, `threshold_crossing_mid_date`, `threshold_crossing_percentile`, `event_end_pentad`, `event_end_date`, `recovery_pentad`, `termination_mid_date`, `recovery_threshold_percentile`, `right_censored_flag`, `intensification_duration_pentads`, `total_duration_pentads`, `total_duration_actual_days`, `mean_intensification_rate_pp_per_pentad`, `minimum_soil_moisture_percentile`, `severity_40pct_deficit_pp_pentads`, `prolonged_after_flash_flag`, `onset_year`, `onset_month`, `antecedent_4pentad_precipitation_mm`, `antecedent_4pentad_VPD_mean_kPa`, `event_precipitation_mm`, `event_VPD_mean_kPa`, `event_VPD_max_kPa`, `event_t2m_mean_C`, `event_t2m_max_C`, `event_ERA5_potential_evaporation_mm`, `event_GLDAS_ET_mm`

## `data/event_catalogue/AEZ26_Phase2C_Flash_Drought_Detection_QC.csv`
Detection quality-control checks
Rows: 13. Columns (3): `check`, `value`, `status`

## `data/event_catalogue/AEZ26_Phase7A_Audit_Reconstructed_GLDAS_v3_Primary_39.csv`
Reconstruction of the primary chronology from the locked pentad table (audit)
Rows: 39. Columns (25): `catalogue`, `event_id`, `anchor_pentad`, `anchor_percentile`, `onset_pentad`, `onset_start_date`, `onset_mid_date`, `threshold_crossing_pentad`, `threshold_crossing_percentile`, `event_end_pentad`, `recovery_pentad`, `right_censored_flag`, `intensification_duration_pentads`, `total_duration_pentads`, `total_duration_actual_days`, `mean_intensification_rate_pp_per_pentad`, `minimum_soil_moisture_percentile`, `severity_40pct_deficit_pp_pentads`, `onset_year`, `onset_month`, `antecedent_4pentad_precipitation_mm`, `event_precipitation_mm`, `event_VPD_mean_kPa`, `event_t2m_mean_C`, `event_ERA5_potential_evaporation_mm`

## `data/event_catalogue/AEZ26_Phase7A_GLDAS_Primary_Candidate_Audit.csv`
Candidate-catalogue audit against the locked 39-event chronology
Rows: 3. Columns (5): `path`, `rows`, `sha256`, `matches_reconstructed_v3_39_exactly`, `status`

## `data/land_water_responses/AEZ26_Phase2F_Cross_Response_Event_Synthesis.csv`
Land–water response metrics (MOD16, MOD13, GRACE, JRC) and seasonal-anomaly links
Rows: 39. Columns (92): `event_id`, `onset_pentad`, `onset_start_date`, `event_end_date`, `total_duration_pentads`, `prolonged_after_flash_flag`, `primary_driver_class`, `onset_season`, `prebaseline_ETPET_z`, `event_weighted_ETPET_z`, `event_weighted_ET_z`, `event_weighted_PET_z`, `minimum_ETPET_z_onset_to_post64`, `minimum_ETPET_drop_from_prebaseline_z`, `minimum_ETPET_native_mid_date`, `lag_onset_to_minimum_ETPET_days`, `lag_event_end_to_minimum_ETPET_days`, `MOD16_recovery_to_seasonal_normal_date`, `MOD16_relative_days_from_event_end_to_seasonal_normal_recovery`, `MOD16_recovery_to_prebaseline_date`, `MOD16_relative_days_from_event_end_to_prebaseline_recovery`, `MOD16_seasonal_normal_recovery_censored_flag`, `prebaseline_ETPET_z_strictQA`, `event_weighted_ETPET_z_strictQA`, `minimum_ETPET_z_strictQA_onset_to_post64`, `candidate_native_records_onset_to_post64`, `prebaseline_NDVI_z`, `prebaseline_EVI_z`, `event_weighted_NDVI_z`, `event_weighted_EVI_z`, `minimum_NDVI_z_onset_to_post96`, `minimum_NDVI_drop_from_prebaseline_z`, `minimum_NDVI_native_anchor_date`, `minimum_NDVI_standard_QA_fraction`, `lag_onset_to_minimum_NDVI_days`, `lag_event_end_to_minimum_NDVI_days`, `minimum_EVI_z_onset_to_post96`, `minimum_EVI_drop_from_prebaseline_z`, `minimum_EVI_native_anchor_date`, `minimum_NDVI_z_QAfrac_ge_025` …

## `data/land_water_responses/AEZ26_Phase2F_GRACE_TWSA_Event_Response_Metrics.csv`
Land–water response metrics (MOD16, MOD13, GRACE, JRC) and seasonal-anomaly links
Rows: 39. Columns (22): `event_id`, `GRACE_response_metric_available_flag`, `primary_driver_class`, `onset_season`, `prebaseline_GRACE_records`, `prebaseline_TWSA_z`, `event_weighted_TWSA_z`, `minimum_TWSA_z_onset_to_post365`, `minimum_TWSA_drop_from_prebaseline_z`, `minimum_TWSA_deseasonalized_cm`, `minimum_TWSA_native_mid_date`, `lag_onset_to_minimum_TWSA_days`, `lag_event_end_to_minimum_TWSA_days`, `other_flash_drought_before_minimum_TWSA_flag`, `GRACE_recovery_to_seasonal_normal_date`, `GRACE_relative_days_from_event_end_to_seasonal_normal_recovery`, `GRACE_recovery_to_prebaseline_date`, `GRACE_relative_days_from_event_end_to_prebaseline_recovery`, `GRACE_seasonal_normal_recovery_censored_flag`, `candidate_GRACE_records_onset_to_post365`, `GRACE_seasonal_normal_recovery_before_event_end_flag`, `GRACE_prebaseline_recovery_before_event_end_flag`

## `data/land_water_responses/AEZ26_Phase2F_GRACE_TWSA_Seasonal_Anomaly_Links.csv`
Land–water response metrics (MOD16, MOD13, GRACE, JRC) and seasonal-anomaly links
Rows: 600. Columns (30): `event_id`, `primary_driver_class`, `onset_season`, `onset_start_date`, `threshold_crossing_end_date`, `event_end_date`, `native_system_index`, `native_start_date`, `native_end_date`, `native_mid_date`, `native_interval_days`, `alignment_phase`, `overlap_event_days`, `overlap_intensification_days`, `overlap_persistence_days`, `event_overlap_fraction_native`, `relative_days_mid_to_onset`, `relative_days_mid_to_event_end`, `overlaps_other_primary_event_flag`, `TWSA_cm`, `mean_mascon_uncertainty_cm`, `TWSA_data_available_flag`, `context_window_start`, `context_window_end`, `calendar_month`, `TWSA_z`, `TWSA_deseasonalized_cm`, `TWSA_monthly_clim_mean_cm`, `TWSA_monthly_clim_sd_cm`, `TWSA_monthly_clim_n`

## `data/land_water_responses/AEZ26_Phase2F_JRC_Qualified_Monthly_Climatology.csv`
Land–water response metrics (MOD16, MOD13, GRACE, JRC) and seasonal-anomaly links
Rows: 11. Columns (5): `calendar_month`, `JRC_clim_mean`, `JRC_clim_sd`, `JRC_clim_median`, `JRC_clim_n`

## `data/land_water_responses/AEZ26_Phase2F_JRC_Qualified_Seasonal_Anomaly_Links.csv`
Land–water response metrics (MOD16, MOD13, GRACE, JRC) and seasonal-anomaly links
Rows: 356. Columns (36): `event_id`, `primary_driver_class`, `onset_season`, `onset_start_date`, `threshold_crossing_end_date`, `event_end_date`, `native_system_index`, `native_month_start`, `native_month_end`, `native_month_mid`, `native_month_days`, `alignment_phase`, `overlap_event_days`, `overlap_intensification_days`, `overlap_persistence_days`, `event_overlap_fraction_native`, `relative_days_mid_to_onset`, `relative_days_mid_to_event_end`, `overlaps_other_primary_event_flag`, `valid_observed_area_km2`, `valid_observation_fraction`, `water_area_km2`, `water_fraction_of_valid_area`, `no_valid_observation_flag`, `low_coverage_flag`, `water_detected_flag`, `coverage_qualified_flag`, `context_window_start`, `context_window_end`, `calendar_month`, `JRC_clim_mean`, `JRC_clim_sd`, `JRC_clim_median`, `JRC_clim_n`, `water_fraction_z`, `water_fraction_deviation_from_monthly_median`

## `data/land_water_responses/AEZ26_Phase2F_JRC_SurfaceWater_Event_Response_Metrics.csv`
Land–water response metrics (MOD16, MOD13, GRACE, JRC) and seasonal-anomaly links
Rows: 39. Columns (22): `event_id`, `primary_driver_class`, `onset_season`, `JRC_response_metric_available_flag`, `prebaseline_JRC_records`, `prebaseline_water_fraction_z`, `event_weighted_water_fraction_z`, `minimum_water_fraction_z_onset_to_post180`, `minimum_water_fraction_drop_from_prebaseline_z`, `minimum_water_fraction_deviation_from_monthly_median`, `minimum_JRC_native_month_mid`, `lag_onset_to_minimum_water_fraction_days`, `lag_event_end_to_minimum_water_fraction_days`, `other_flash_drought_before_minimum_JRC_flag`, `JRC_recovery_to_seasonal_normal_date`, `JRC_relative_days_from_event_end_to_seasonal_normal_recovery`, `JRC_recovery_to_prebaseline_date`, `JRC_relative_days_from_event_end_to_prebaseline_recovery`, `JRC_seasonal_normal_recovery_censored_flag`, `candidate_qualified_JRC_records_onset_to_post180`, `JRC_seasonal_normal_recovery_before_event_end_flag`, `JRC_prebaseline_recovery_before_event_end_flag`

## `data/land_water_responses/AEZ26_Phase2F_MOD13_Event_Response_Metrics.csv`
Land–water response metrics (MOD16, MOD13, GRACE, JRC) and seasonal-anomaly links
Rows: 39. Columns (29): `event_id`, `primary_driver_class`, `onset_season`, `prebaseline_NDVI_z`, `prebaseline_EVI_z`, `event_weighted_NDVI_z`, `event_weighted_EVI_z`, `minimum_NDVI_z_onset_to_post96`, `minimum_NDVI_drop_from_prebaseline_z`, `minimum_NDVI_native_anchor_date`, `minimum_NDVI_standard_QA_fraction`, `lag_onset_to_minimum_NDVI_days`, `lag_event_end_to_minimum_NDVI_days`, `minimum_EVI_z_onset_to_post96`, `minimum_EVI_drop_from_prebaseline_z`, `minimum_EVI_native_anchor_date`, `minimum_NDVI_z_QAfrac_ge_025`, `minimum_NDVI_z_QAfrac_ge_050`, `minimum_EVI_z_QAfrac_ge_025`, `minimum_EVI_z_QAfrac_ge_050`, `minimum_NDVI_z_strictQA`, `MOD13_recovery_to_seasonal_normal_date`, `MOD13_relative_days_from_event_end_to_seasonal_normal_recovery`, `MOD13_recovery_to_prebaseline_date`, `MOD13_relative_days_from_event_end_to_prebaseline_recovery`, `MOD13_seasonal_normal_recovery_censored_flag`, `candidate_standardQA_records_onset_to_post96`, `MOD13_seasonal_normal_recovery_before_event_end_flag`, `MOD13_prebaseline_recovery_before_event_end_flag`

## `data/land_water_responses/AEZ26_Phase2F_MOD13_Seasonal_Anomaly_Links.csv`
Land–water response metrics (MOD16, MOD13, GRACE, JRC) and seasonal-anomaly links
Rows: 445. Columns (34): `event_id`, `primary_driver_class`, `onset_season`, `onset_start_date`, `threshold_crossing_end_date`, `event_end_date`, `native_composite_start_date`, `native_system_index`, `nominal_temporal_resolution_days`, `alignment_phase`, `relative_days_anchor_to_onset`, `relative_days_anchor_to_event_end`, `anchor_inside_current_event_flag`, `anchor_inside_other_primary_event_flag`, `NDVI_allValid`, `EVI_allValid`, `all_valid_fraction`, `NDVI_standardQA`, `EVI_standardQA`, `standard_QA_fraction`, `standard_QA_data_available_flag`, `NDVI_strictQA`, `EVI_strictQA`, `strict_QA_fraction`, `strict_QA_data_available_flag`, `SummaryQA_good_fraction`, `SummaryQA_marginal_fraction`, `context_window_start`, `context_window_end`, `seasonal_slot_16day`, `NDVI_standardQA_z`, `EVI_standardQA_z`, `NDVI_strictQA_z`, `EVI_strictQA_z`

## `data/land_water_responses/AEZ26_Phase2F_MOD16_Event_Response_Metrics.csv`
Land–water response metrics (MOD16, MOD13, GRACE, JRC) and seasonal-anomaly links
Rows: 39. Columns (23): `event_id`, `primary_driver_class`, `onset_season`, `prebaseline_ETPET_z`, `event_weighted_ETPET_z`, `event_weighted_ET_z`, `event_weighted_PET_z`, `minimum_ETPET_z_onset_to_post64`, `minimum_ETPET_drop_from_prebaseline_z`, `minimum_ETPET_native_mid_date`, `lag_onset_to_minimum_ETPET_days`, `lag_event_end_to_minimum_ETPET_days`, `MOD16_recovery_to_seasonal_normal_date`, `MOD16_relative_days_from_event_end_to_seasonal_normal_recovery`, `MOD16_recovery_to_prebaseline_date`, `MOD16_relative_days_from_event_end_to_prebaseline_recovery`, `MOD16_seasonal_normal_recovery_censored_flag`, `prebaseline_ETPET_z_strictQA`, `event_weighted_ETPET_z_strictQA`, `minimum_ETPET_z_strictQA_onset_to_post64`, `candidate_native_records_onset_to_post64`, `MOD16_seasonal_normal_recovery_before_event_end_flag`, `MOD16_prebaseline_recovery_before_event_end_flag`

## `data/land_water_responses/AEZ26_Phase2F_MOD16_Seasonal_Anomaly_Links.csv`
Land–water response metrics (MOD16, MOD13, GRACE, JRC) and seasonal-anomaly links
Rows: 690. Columns (44): `event_id`, `primary_driver_class`, `onset_season`, `onset_start_date`, `threshold_crossing_end_date`, `event_end_date`, `native_start_date`, `native_end_date`, `native_mid_date`, `native_days`, `alignment_phase`, `overlap_event_days`, `overlap_intensification_days`, `overlap_persistence_days`, `event_overlap_fraction_native`, `intensification_overlap_fraction_native`, `persistence_overlap_fraction_native`, `relative_days_mid_to_onset`, `relative_days_mid_to_event_end`, `overlaps_other_primary_event_flag`, `ET_primary_mm_composite`, `PET_primary_mm_composite`, `ET_primary_mm_day`, `PET_primary_mm_day`, `ET_PET_ratio_primary`, `primary_valid_fraction`, `primary_data_available_flag`, `ET_strictQA_mm_composite`, `PET_strictQA_mm_composite`, `ET_strictQA_mm_day`, `PET_strictQA_mm_day`, `ET_PET_ratio_strictQA`, `strict_QA_fraction`, `strict_QA_data_available_flag`, `MODLAND_good_fraction`, `clear_pixel_fraction`, `SCF_0_or_1_fraction`, `context_window_start`, `context_window_end`, `seasonal_slot_8day` …

## `data/land_water_responses/AEZ26_Phase2F_QC.csv`
Land–water response metrics (MOD16, MOD13, GRACE, JRC) and seasonal-anomaly links
Rows: 19. Columns (4): `check`, `value`, `status`, `note`

## `data/pentad_indicators/AEZ26_Pentad_Hydroclimate_Indicators_2000_2025.csv`
GLDAS/CHIRPS/ERA5-Land regional pentad hydroclimate indicators 2000–2025 (73 pentads per year)
Rows: 1898. Columns (59): `pentad_id`, `year`, `pentad_of_year`, `pentad_start`, `pentad_end`, `n_days`, `precipitation_sum_mm`, `precipitation_mean_mm_day`, `t2m_mean_C`, `t2m_max_C`, `t2m_min_C`, `dewpoint_mean_C`, `relative_humidity_mean_pct`, `VPD_mean_kPa`, `VPD_max_kPa`, `wind_speed_mean_m_s`, `solar_radiation_sum_MJ_m2`, `solar_radiation_mean_MJ_m2_day`, `net_solar_radiation_sum_MJ_m2`, `net_thermal_radiation_sum_MJ_m2`, `net_radiation_sum_MJ_m2`, `net_radiation_mean_MJ_m2_day`, `total_evaporation_sum_mm`, `total_evaporation_mean_mm_day`, `ERA5_potential_evaporation_sum_mm`, `ERA5_potential_evaporation_mean_mm_day`, `SM_0_10cm_mean_mm`, `SM_10_40cm_mean_mm`, `SM_40_100cm_mean_mm`, `SM_100_200cm_mean_mm`, `SM_0_40cm_mean_mm`, `SM_0_100cm_mean_mm`, `SM_0_200cm_mean_mm`, `RootMoist_mean_mm`, `surface_runoff_sum_mm`, `surface_runoff_mean_mm_day`, `baseflow_sum_mm`, `baseflow_mean_mm_day`, `total_runoff_sum_mm`, `total_runoff_mean_mm_day` …

## `data/pentad_indicators/AEZ26_Robustness_Annual_FD_Counts_1981_2025.csv`
Annual summaries from the extended record
Rows: 45. Columns (2): `year`, `flash_drought_count`

## `data/pentad_indicators/AEZ26_Robustness_Annual_Hydroclimate_1981_2025.csv`
Annual summaries from the extended record
Rows: 45. Columns (5): `year`, `temperature_C`, `VPD_kPa`, `precipitation_mm`, `potential_evaporation_mm`

## `data/pentad_indicators/AEZ26_Robustness_ERA5Land_Pentad_Indicators_1981_2025.csv`
ERA5-Land and CHIRPS regional pentad indicators 1981–2025 (Phase 7A extended record; stored table for Eqs 6/7)
Rows: 3285. Columns (28): `system:index`, `ERA5_SM_0_100_mean_mm`, `ERA5_potential_evaporation_sum_mm`, `VPD_dailymean_max_kPa`, `VPD_mean_kPa`, `aoi_asset`, `chirps_daily_images`, `chirps_source`, `complete_pentad_flag`, `era5_daily_images`, `era5_source`, `leap_day_included_flag`, `n_days`, `pentad_end`, `pentad_label`, `pentad_mid_date`, `pentad_of_year`, `pentad_start`, `precipitation_sum_mm`, `relative_humidity_mean_pct`, `t2m_max_C`, `t2m_mean_C`, `year`, `.geo`, `source_chunk_file`, `ERA5_SM_pct_LONG45`, `ERA5_SM_pct_OVERLAP26`, `ERA5_SM_z_OVERLAP26`

## `data/phase7a_chunks_sanitized/AEZ26_Phase7A_ERA5Land_CHIRPS_Pentad_1981_1985.csv`

Rows: 365. Columns (24): `system:index`, `ERA5_SM_0_100_mean_mm`, `ERA5_potential_evaporation_sum_mm`, `VPD_dailymean_max_kPa`, `VPD_mean_kPa`, `aoi_asset`, `chirps_daily_images`, `chirps_source`, `complete_pentad_flag`, `era5_daily_images`, `era5_source`, `leap_day_included_flag`, `n_days`, `pentad_end`, `pentad_label`, `pentad_mid_date`, `pentad_of_year`, `pentad_start`, `precipitation_sum_mm`, `relative_humidity_mean_pct`, `t2m_max_C`, `t2m_mean_C`, `year`, `.geo`

## `data/phase7a_chunks_sanitized/AEZ26_Phase7A_ERA5Land_CHIRPS_Pentad_1986_1990.csv`

Rows: 365. Columns (24): `system:index`, `ERA5_SM_0_100_mean_mm`, `ERA5_potential_evaporation_sum_mm`, `VPD_dailymean_max_kPa`, `VPD_mean_kPa`, `aoi_asset`, `chirps_daily_images`, `chirps_source`, `complete_pentad_flag`, `era5_daily_images`, `era5_source`, `leap_day_included_flag`, `n_days`, `pentad_end`, `pentad_label`, `pentad_mid_date`, `pentad_of_year`, `pentad_start`, `precipitation_sum_mm`, `relative_humidity_mean_pct`, `t2m_max_C`, `t2m_mean_C`, `year`, `.geo`

## `data/phase7a_chunks_sanitized/AEZ26_Phase7A_ERA5Land_CHIRPS_Pentad_1991_1995.csv`

Rows: 365. Columns (24): `system:index`, `ERA5_SM_0_100_mean_mm`, `ERA5_potential_evaporation_sum_mm`, `VPD_dailymean_max_kPa`, `VPD_mean_kPa`, `aoi_asset`, `chirps_daily_images`, `chirps_source`, `complete_pentad_flag`, `era5_daily_images`, `era5_source`, `leap_day_included_flag`, `n_days`, `pentad_end`, `pentad_label`, `pentad_mid_date`, `pentad_of_year`, `pentad_start`, `precipitation_sum_mm`, `relative_humidity_mean_pct`, `t2m_max_C`, `t2m_mean_C`, `year`, `.geo`

## `data/phase7a_chunks_sanitized/AEZ26_Phase7A_ERA5Land_CHIRPS_Pentad_1996_2000.csv`

Rows: 365. Columns (24): `system:index`, `ERA5_SM_0_100_mean_mm`, `ERA5_potential_evaporation_sum_mm`, `VPD_dailymean_max_kPa`, `VPD_mean_kPa`, `aoi_asset`, `chirps_daily_images`, `chirps_source`, `complete_pentad_flag`, `era5_daily_images`, `era5_source`, `leap_day_included_flag`, `n_days`, `pentad_end`, `pentad_label`, `pentad_mid_date`, `pentad_of_year`, `pentad_start`, `precipitation_sum_mm`, `relative_humidity_mean_pct`, `t2m_max_C`, `t2m_mean_C`, `year`, `.geo`

## `data/phase7a_chunks_sanitized/AEZ26_Phase7A_ERA5Land_CHIRPS_Pentad_2001_2005.csv`

Rows: 365. Columns (24): `system:index`, `ERA5_SM_0_100_mean_mm`, `ERA5_potential_evaporation_sum_mm`, `VPD_dailymean_max_kPa`, `VPD_mean_kPa`, `aoi_asset`, `chirps_daily_images`, `chirps_source`, `complete_pentad_flag`, `era5_daily_images`, `era5_source`, `leap_day_included_flag`, `n_days`, `pentad_end`, `pentad_label`, `pentad_mid_date`, `pentad_of_year`, `pentad_start`, `precipitation_sum_mm`, `relative_humidity_mean_pct`, `t2m_max_C`, `t2m_mean_C`, `year`, `.geo`

## `data/phase7a_chunks_sanitized/AEZ26_Phase7A_ERA5Land_CHIRPS_Pentad_2006_2010.csv`

Rows: 365. Columns (24): `system:index`, `ERA5_SM_0_100_mean_mm`, `ERA5_potential_evaporation_sum_mm`, `VPD_dailymean_max_kPa`, `VPD_mean_kPa`, `aoi_asset`, `chirps_daily_images`, `chirps_source`, `complete_pentad_flag`, `era5_daily_images`, `era5_source`, `leap_day_included_flag`, `n_days`, `pentad_end`, `pentad_label`, `pentad_mid_date`, `pentad_of_year`, `pentad_start`, `precipitation_sum_mm`, `relative_humidity_mean_pct`, `t2m_max_C`, `t2m_mean_C`, `year`, `.geo`

## `data/phase7a_chunks_sanitized/AEZ26_Phase7A_ERA5Land_CHIRPS_Pentad_2011_2015.csv`

Rows: 365. Columns (24): `system:index`, `ERA5_SM_0_100_mean_mm`, `ERA5_potential_evaporation_sum_mm`, `VPD_dailymean_max_kPa`, `VPD_mean_kPa`, `aoi_asset`, `chirps_daily_images`, `chirps_source`, `complete_pentad_flag`, `era5_daily_images`, `era5_source`, `leap_day_included_flag`, `n_days`, `pentad_end`, `pentad_label`, `pentad_mid_date`, `pentad_of_year`, `pentad_start`, `precipitation_sum_mm`, `relative_humidity_mean_pct`, `t2m_max_C`, `t2m_mean_C`, `year`, `.geo`

## `data/phase7a_chunks_sanitized/AEZ26_Phase7A_ERA5Land_CHIRPS_Pentad_2016_2020.csv`

Rows: 365. Columns (24): `system:index`, `ERA5_SM_0_100_mean_mm`, `ERA5_potential_evaporation_sum_mm`, `VPD_dailymean_max_kPa`, `VPD_mean_kPa`, `aoi_asset`, `chirps_daily_images`, `chirps_source`, `complete_pentad_flag`, `era5_daily_images`, `era5_source`, `leap_day_included_flag`, `n_days`, `pentad_end`, `pentad_label`, `pentad_mid_date`, `pentad_of_year`, `pentad_start`, `precipitation_sum_mm`, `relative_humidity_mean_pct`, `t2m_max_C`, `t2m_mean_C`, `year`, `.geo`

## `data/phase7a_chunks_sanitized/AEZ26_Phase7A_ERA5Land_CHIRPS_Pentad_2021_2025.csv`

Rows: 365. Columns (24): `system:index`, `ERA5_SM_0_100_mean_mm`, `ERA5_potential_evaporation_sum_mm`, `VPD_dailymean_max_kPa`, `VPD_mean_kPa`, `aoi_asset`, `chirps_daily_images`, `chirps_source`, `complete_pentad_flag`, `era5_daily_images`, `era5_source`, `leap_day_included_flag`, `n_days`, `pentad_end`, `pentad_label`, `pentad_mid_date`, `pentad_of_year`, `pentad_start`, `precipitation_sum_mm`, `relative_humidity_mean_pct`, `t2m_max_C`, `t2m_mean_C`, `year`, `.geo`

## `data/phase7a_chunks_sanitized/CHUNK_HASH_MAP.csv`

Rows: 9. Columns (5): `file`, `sha256_original_export_not_distributed`, `sha256_this_sanitised_file`, `data_rows`, `only_column_changed`

## `data/statistical_outputs/AEZ26_Phase2G_Cross_Response_Coupling.csv`
Statistical association tables, robustness and cohort summaries
Rows: 6. Columns (10): `pair_label`, `response_x`, `response_y`, `n`, `rho`, `p_perm`, `ci_low`, `ci_high`, `p_fdr_bh`, `fdr_0_05_flag`

## `data/statistical_outputs/AEZ26_Phase2G_DriverClass_Response_Comparisons.csv`
Statistical association tables, robustness and cohort summaries
Rows: 4. Columns (14): `outcome`, `outcome_label`, `n`, `k`, `H`, `p_perm`, `epsilon2`, `group_sizes`, `median_compound_Pdeficit_highPE`, `median_high_PE_only`, `median_neither_large_anomaly`, `median_precipitation_deficit_only`, `p_fdr_bh`, `fdr_0_05_flag`

## `data/statistical_outputs/AEZ26_Phase2G_EventPhysics_Response_Associations.csv`
Statistical association tables, robustness and cohort summaries
Rows: 8. Columns (12): `family`, `predictor`, `predictor_label`, `outcome`, `outcome_label`, `n`, `rho`, `p_perm`, `ci_low`, `ci_high`, `p_fdr_bh`, `fdr_0_05_flag`

## `data/statistical_outputs/AEZ26_Phase2G_Event_Statistical_Analysis_Table.csv`
Statistical association tables, robustness and cohort summaries
Rows: 39. Columns (158): `event_id`, `onset_pentad_driver`, `onset_mid_date`, `onset_year`, `onset_month`, `onset_season_driver`, `threshold_crossing_pentad`, `intensification_duration_pentads`, `intensification_actual_days`, `total_duration_pentads_driver`, `severity_40pct_deficit_pp_pentads`, `mean_intensification_rate_pp_per_pentad`, `prolonged_after_flash_flag_driver`, `seasonal_reference_window_count`, `intensification_precipitation_mm`, `intensification_PE_mm`, `intensification_VPD_mean_kPa`, `intensification_t2m_mean_C`, `intensification_net_radiation_mean_MJ_m2_day`, `intensification_wind_mean_m_s`, `intensification_RH_mean_pct`, `P_reference_mean_mm`, `P_reference_sd_mm`, `PE_reference_mean_mm`, `PE_reference_sd_mm`, `P_standardized_anomaly_z`, `PE_standardized_anomaly_z`, `VPD_standardized_anomaly_z`, `temperature_standardized_anomaly_z`, `net_radiation_standardized_anomaly_z`, `wind_standardized_anomaly_z`, `RH_standardized_anomaly_z`, `P_empirical_percentile`, `PE_empirical_percentile`, `VPD_empirical_percentile`, `temperature_empirical_percentile`, `net_radiation_empirical_percentile`, `wind_empirical_percentile`, `RH_empirical_percentile`, `large_precipitation_deficit_flag` …

## `data/statistical_outputs/AEZ26_Phase2G_Primary_Driver_Response_Associations.csv`
Statistical association tables, robustness and cohort summaries
Rows: 16. Columns (12): `family`, `predictor`, `predictor_label`, `outcome`, `outcome_label`, `n`, `rho`, `p_perm`, `ci_low`, `ci_high`, `p_fdr_bh`, `fdr_0_05_flag`

## `data/statistical_outputs/AEZ26_Phase2G_QC.csv`
Statistical association tables, robustness and cohort summaries
Rows: 15. Columns (4): `check`, `value`, `status`, `note`

## `data/statistical_outputs/AEZ26_Phase2G_Response_Cohort_Summary.csv`
Statistical association tables, robustness and cohort summaries
Rows: 9. Columns (4): `cohort`, `outcome`, `n_events`, `median_response_depth_z`

## `data/statistical_outputs/AEZ26_Phase2G_Secondary_Atmospheric_Response_Associations.csv`
Statistical association tables, robustness and cohort summaries
Rows: 12. Columns (12): `family`, `predictor`, `predictor_label`, `outcome`, `outcome_label`, `n`, `rho`, `p_perm`, `ci_low`, `ci_high`, `p_fdr_bh`, `fdr_0_05_flag`

## `data/statistical_outputs/closure_checks/assoc_reproduction.csv`
See folder description.
Rows: 46. Columns (22): `family`, `predictor`, `outcome`, `n`, `n_stored`, `rho`, `rho_stored`, `p_perm`, `p_stored`, `ci_low`, `ci_low_stored`, `ci_high`, `ci_high_stored`, `q_stored`, `q_from_own_p`, `q_from_stored_p`, `rho_diff`, `p_diff`, `mc_se`, `p_within_3se`, `q_own_le_0.05`, `q_stored_le_0.05`

## `data/statistical_outputs/closure_checks/chron_event_diagnosis.csv`
See folder description.
Rows: 39. Columns (16): `event`, `onset`, `gldas_cross_pct`, `gldas_end`, `gldas_rate`, `gldas_dur`, `era5_pct_at_gldas_cross`, `era5_min_pct_cross_pm2`, `era5_pct_at_anchor`, `gldas_pct_at_anchor`, `nearest_era5_onset`, `offset_pentads`, `matched_pm2`, `class_`, `reject_reason`, `gldas_cross_margin_below20`

## `data/statistical_outputs/closure_checks/chron_res.json`

Text/JSON/Markdown file.

## `data/statistical_outputs/closure_checks/consensus_associations.csv`
See folder description.
Rows: 16. Columns (13): `predictor`, `outcome`, `n_full`, `rho_full`, `rho_stored`, `nC`, `rho_C`, `ciC_low`, `ciC_high`, `nN`, `rho_N`, `C_interval_includes_zero`, `rule_outcome`

## `data/statistical_outputs/closure_checks/consensus_comparisons.csv`
See folder description.
Rows: 92. Columns (8): `set`, `variable`, `nC`, `nN`, `medianC`, `medianN`, `p_MWU`, `q_BH_within_set`

## `data/statistical_outputs/closure_checks/consensus_driver_classes.csv`
See folder description.
Rows: 2. Columns (5): `row_0`, `compound_Pdeficit_highPE`, `high_PE_only`, `neither_large_anomaly`, `precipitation_deficit_only`

## `data/statistical_outputs/closure_checks/consensus_masks.json`

Text/JSON/Markdown file.

## `data/statistical_outputs/closure_checks/cross_exact.csv`
See folder description.
Rows: 6. Columns (8): `pair`, `n`, `rho`, `p_stored`, `p_2M`, `se`, `q_stored`, `q_2M`

## `data/statistical_outputs/closure_checks/seasctl_events.csv`
See folder description.
Rows: 145. Columns (12): `event_id`, `n_pre`, `n_post`, `pre_min`, `post_min_links`, `post_min_stored`, `stored_match`, `E_post`, `E_pre`, `excess_post`, `excess_pre`, `product`

## `data/statistical_outputs/closure_checks/seasctl_summary.csv`
See folder description.
Rows: 12. Columns (15): `product`, `check`, `n`, `median`, `n_negative`, `p_wilcoxon`, `p_sign`, `median_observed_min`, `median_iid_expected_min`, `median_excess`, `median_n_records`, `stored_min_reproduced_from_links`, `median_excess_pre`, `median_excess_post`, `median_n_pre`

## `data/statistical_outputs/closure_checks/seasctl_timing_fraction.csv`
See folder description.
Rows: 4. Columns (7): `product`, `n`, `median_lag_days`, `median_window_days`, `median_fraction`, `iqr`, `p_wilcoxon_vs_0p5`

## `documentation/method_configs/AEZ26_Phase2D_Method_Config.txt`

Text/JSON/Markdown file.

## `documentation/method_configs/AEZ26_Phase2F_Method_Config.txt`

Text/JSON/Markdown file.

## `documentation/method_configs/AEZ26_Phase2G_Method_Config.txt`

Text/JSON/Markdown file.

## `historical_inputs/README_HISTORICAL_INPUTS.md`

Text/JSON/Markdown file.

## `historical_inputs/phase7a_locked_input/AEZ26_Pentad_Hydroclimate_Indicators_2000_2025.csv`
GLDAS/CHIRPS/ERA5-Land regional pentad hydroclimate indicators 2000–2025 (73 pentads per year)
Rows: 1898. Columns (59): `pentad_id`, `year`, `pentad_of_year`, `pentad_start`, `pentad_end`, `n_days`, `precipitation_sum_mm`, `precipitation_mean_mm_day`, `t2m_mean_C`, `t2m_max_C`, `t2m_min_C`, `dewpoint_mean_C`, `relative_humidity_mean_pct`, `VPD_mean_kPa`, `VPD_max_kPa`, `wind_speed_mean_m_s`, `solar_radiation_sum_MJ_m2`, `solar_radiation_mean_MJ_m2_day`, `net_solar_radiation_sum_MJ_m2`, `net_thermal_radiation_sum_MJ_m2`, `net_radiation_sum_MJ_m2`, `net_radiation_mean_MJ_m2_day`, `total_evaporation_sum_mm`, `total_evaporation_mean_mm_day`, `ERA5_potential_evaporation_sum_mm`, `ERA5_potential_evaporation_mean_mm_day`, `SM_0_10cm_mean_mm`, `SM_10_40cm_mean_mm`, `SM_40_100cm_mean_mm`, `SM_100_200cm_mean_mm`, `SM_0_40cm_mean_mm`, `SM_0_100cm_mean_mm`, `SM_0_200cm_mean_mm`, `RootMoist_mean_mm`, `surface_runoff_sum_mm`, `surface_runoff_mean_mm_day`, `baseflow_sum_mm`, `baseflow_mean_mm_day`, `total_runoff_sum_mm`, `total_runoff_mean_mm_day` …

## `metadata/source_datasets.csv`

Rows: 9. Columns (12): `dataset`, `provider`, `product_identifier`, `temporal_coverage`, `spatial_resolution`, `reference_or_doi (from manuscript)`, `licence_or_usage_restriction_status`, `what_this_release_contains`, `official_download_URL`, `access_date`, `provider_terms_as_located`, `terms_source_url_checked_2026-11-14`

## Added in v1.0.1: `data/eq6_eq7_verification/eq7_fullrecord/`
| File | Content |
|---|---|
| `AEZ26_Eq7FR_ABC_12pentads.csv` | Author-run Earth Engine export (unedited): 12 pentads (1982–2025; June–August and November–December among them) with pathways A, B and C of T, Td, RH, VPD mean and maximum and 0–100 cm storage; same 31 columns as the 23-pentad file. SHA-256 `e7e48abec3f9e2cf8c1c208d88ea4e646f51e5c8a371c3b3d01a8d20e9eff17f`. |
| `AEZ26_Eq7_Recomputed_3285pentads.csv` | Offline Eq. 7 recomputation per pixel and day, zone-averaged per pentad, for all 3,285 pentads (columns `S_*` sample footprint weights, `N_*` native-cell weights; T, Td, RH, VPD, VPD maximum, T maximum; calendar and pixel counts). SHA-256 `f7c9dd69bb07b737a16dd54e656a344abbefae06d3f6dcee995aeea6b3348d2a`. Produced by `scripts/eq6_eq7_audit/eq7_fullrecord_recompute.py` from the withheld exports. |
| `AEZ26_Eq7_Recomputed_vs_Stored_3285pentads.csv` | The recomputation merged with the stored extended ERA5-Land series (reference output of `eq7_fullrecord_checks.py`). |
| `AEZ26_Eq7_ABC_35pentads_with_offline.csv` | The 23 + 12 pentads with pathways A, B, C, the stored values and the offline recomputation (reference output of `eq7_fullrecord_checks.py`). |
| `eq7_fullrecord_checks_part1.json`, `eq7_fullrecord_checks_part2.json` | Reference outputs: agreement statistics (S1–S3) and offset, step, drift and trend results (S4–S7). |
| `pixel_export_sha256.csv` | Names, sizes, row counts and SHA-256 of the 44 per-year exports (45 with the 2000 file) and the weights table, all withheld. |

`data/eq6_eq7_verification/eq6/eq6_35pentad_soilwater_offsets.csv`: B − A soil-water offsets of the 35 pentads by month, period and soil-water state (reference output of `scripts/eq6_eq7_audit/eq6_35pentad_soilwater_offsets.py`).
