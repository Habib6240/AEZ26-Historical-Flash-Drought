// ============================================================================
// AEZ-26  Eq. 7 PART B  ONE-YEAR PILOT (v01-pilot)  -- derived from v01, which is kept unchanged.
// Only differences from v01: RUN_PART fixed to 'B'; PILOT_YEAR added; the final
// block queues ONE export (PILOT_YEAR) instead of 45; diagnostic prints added.
// AOI, ERA5_SCALE, 15 km buffer, 0.1-deg footprint weights, columns and pentad
// calendar are byte-identical to v01. Part A is NOT run here.
// Prepared 2026-11-12 for the author to run in the Earth Engine Code Editor.
// Output files are the exact names expected by the Eq. 6/7 audit.
// Nothing here changes the Phase 7A method: same collection, AOI asset, scale
// (11132 m), reducer (mean), 73-pentad calendar, leap-day rule (P12 = 6 days,
// P13+ shifted one actual day).
//
// PART A: layer-wise pentad means  -> 9 CSV files (365 rows each)
//         AEZ26_Phase7A_ERA5Land_Layers_Pentad_<y0>_<y0+4>.csv
// PART B: per-pixel daily T and Td -> 45 yearly CSV files (to be concatenated
//         in Python into AEZ26_ERA5Land_Daily_Pixel_T_Td_1981_2025.csv)
//
// Run ONE part at a time from the Tasks tab. Keep the exported CSVs unedited and
// send them for audit together with the SHA-256 of each file (certutil/sha256sum).
// AOI asset id is the author's private asset; it is not disclosed outside the repo.
// ============================================================================
var AOI_ASSET = 'projects/<YOUR-EE-PROJECT>/assets/<YOUR-AEZ26-ASSET>';
var ERA5_SCALE = 11132;
var DRIVE_FOLDER = 'AEZ26_Final_Research_Data';
var RUN_PART = 'B';            // pilot: Part B only
var PILOT_YEAR = 2000;         // single pilot year (leap year, tests the P12/P13 rule)

var aoiFC = ee.FeatureCollection(AOI_ASSET);
var aoi = aoiFC.geometry();
var eraRaw = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR');

function isLeapYear(y) {
  y = ee.Number(y);
  return y.mod(4).eq(0).and(y.mod(100).neq(0).or(y.mod(400).eq(0)));
}
// identical to the Phase 7A pentadWindow()
function pentadWindow(y, p) {
  y = ee.Number(y); p = ee.Number(p);
  var leap = isLeapYear(y);
  var shift = ee.Number(ee.Algorithms.If(leap.and(p.gte(13)), 1, 0));
  var nDays = ee.Number(ee.Algorithms.If(leap.and(p.eq(12)), 6, 5));
  var start = ee.Date.fromYMD(y, 1, 1).advance(p.subtract(1).multiply(5).add(shift), 'day');
  return {start: start, endExclusive: start.advance(nDays, 'day'), nDays: nDays};
}

// ---------------------------- PART A ---------------------------------------
function layerFeature(y, p) {
  var w = pentadWindow(y, p);
  var e = eraRaw.filterDate(w.start, w.endExclusive);
  var img = ee.Image.cat([
    e.select('volumetric_soil_water_layer_1').mean().rename('swvl1_mean_m3m3'),
    e.select('volumetric_soil_water_layer_2').mean().rename('swvl2_mean_m3m3'),
    e.select('volumetric_soil_water_layer_3').mean().rename('swvl3_mean_m3m3')]);
  var s = img.reduceRegion({reducer: ee.Reducer.mean(), geometry: aoi,
    scale: ERA5_SCALE, maxPixels: 1e8, tileScale: 4});
  y = ee.Number(y); p = ee.Number(p);
  return ee.Feature(null, {
    year: y, pentad_of_year: p,
    pentad_label: y.format('%d').cat('_P').cat(p.format('%02d')),
    pentad_start: w.start.format('YYYY-MM-dd'),
    pentad_end: w.endExclusive.advance(-1, 'day').format('YYYY-MM-dd'),
    n_days: w.nDays, era5_daily_images: e.size(),
    swvl1_mean_m3m3: s.get('swvl1_mean_m3m3'),
    swvl2_mean_m3m3: s.get('swvl2_mean_m3m3'),
    swvl3_mean_m3m3: s.get('swvl3_mean_m3m3')});
}
function exportLayers(y0) {
  var fc = ee.FeatureCollection(ee.List.sequence(y0, y0 + 4).map(function (y) {
    return ee.List.sequence(1, 73).map(function (p) { return layerFeature(y, p); });
  }).flatten());
  var name = 'AEZ26_Phase7A_ERA5Land_Layers_Pentad_' + y0 + '_' + (y0 + 4);
  Export.table.toDrive({collection: fc, description: name, folder: DRIVE_FOLDER,
    fileNamePrefix: name, fileFormat: 'CSV',
    selectors: ['year','pentad_of_year','pentad_label','pentad_start','pentad_end',
                'n_days','era5_daily_images','swvl1_mean_m3m3','swvl2_mean_m3m3','swvl3_mean_m3m3']});
}

// ---------------------------- PART B ---------------------------------------
// ERA5-Land native pixels are 0.1 deg. Pixels are sampled over a buffered AOI
// (superset); coverage_weight = area(pixel footprint ∩ AOI) / area(footprint),
// pixels with weight 0 are dropped afterwards in Python. The audit then checks
// that the weighted mean of per-pixel pentad temperature reproduces the stored
// t2m_mean_C of the Phase 7A tables. If it does not, the weights must be revised.
var proj = eraRaw.first().projection();
var region = aoi.buffer(15000);
function pixelRows(img) {
  var d = ee.Date(img.get('system:time_start'));
  var px = img.select(['temperature_2m', 'dewpoint_temperature_2m'])
    .sample({region: region, projection: proj, scale: ERA5_SCALE,
             geometries: true, dropNulls: false});
  return px.map(function (f) {
    var c = f.geometry().coordinates();
    var lon = ee.Number(c.get(0)), lat = ee.Number(c.get(1));
    var rect = ee.Geometry.Rectangle([lon.subtract(0.05), lat.subtract(0.05),
                                      lon.add(0.05), lat.add(0.05)], null, false);
    var wgt = rect.intersection(aoi, ee.ErrorMargin(1)).area(1).divide(rect.area(1));
    return ee.Feature(null, {
      date: d.format('YYYY-MM-dd'),
      pixel_id: lon.format('%.2f').cat('_').cat(lat.format('%.2f')),
      lon: lon, lat: lat, coverage_weight: wgt,
      temperature_2m_K: f.get('temperature_2m'),
      dewpoint_temperature_2m_K: f.get('dewpoint_temperature_2m')});
  }).filter(ee.Filter.gt('coverage_weight', 0));
}
function exportPixels(y) {
  var fc = eraRaw.filterDate(y + '-01-01', (y + 1) + '-01-01')
    .map(pixelRows).flatten();
  var name = 'AEZ26_ERA5Land_Daily_Pixel_T_Td_' + y;
  Export.table.toDrive({collection: fc, description: name, folder: DRIVE_FOLDER,
    fileNamePrefix: name, fileFormat: 'CSV',
    selectors: ['date','pixel_id','lon','lat','coverage_weight',
                'temperature_2m_K','dewpoint_temperature_2m_K']});
}

// ---------------------------- PILOT RUN -------------------------------------
var pilotImgs = eraRaw.filterDate(PILOT_YEAR + '-01-01', (PILOT_YEAR + 1) + '-01-01');
print('Pilot year', PILOT_YEAR, '| daily images (expect 366 in 2000):', pilotImgs.size());
print('Pixels with coverage_weight > 0 on first day:', pixelRows(pilotImgs.first()).size());
print('First-day rows (inspect pixel_id, coverage_weight, T, Td):', pixelRows(pilotImgs.first()).limit(25));
exportPixels(PILOT_YEAR);
print('Pilot: 1 export task queued (AEZ26_ERA5Land_Daily_Pixel_T_Td_' + PILOT_YEAR + '). Run it from the Tasks tab.');
