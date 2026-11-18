// ============================================================================
// AEZ-26  Equation 7 FULL-RECORD SOURCE VERIFICATION EXPORT  (v01)
// ERA5-Land DAILY_AGGR, 1981-2025.  ONE script, three run modes (RUN_PART).
//
// STATUS (release v1.0.1; header text only, no code line changed): the three run modes were run by the author in Earth Engine on 2026-11-15
// (WEIGHTS, PIXELS in two batches, DIAG). The exported CSVs and their SHA-256 values are the record of what was executed
// (data/eq6_eq7_verification/eq7_fullrecord/ in the dataset record); the per-pixel exports are withheld. The script file was not run in the release QA (syntax check only).
//
// Purpose: obtain the per-pixel daily 2 m temperature and dew point needed to
// recompute Equation 7 offline for all 3,285 pentads, and to give exact Earth
// Engine spatial-reduction pathways A, B and C for 12 additional pentads.
// Nothing here changes the Phase 7A method, any stored series or any canonical file.
//
// RUN MODES (set RUN_PART, press Run, then start the queued tasks in the Tasks tab):
//   'WEIGHTS' : 1 task  - one-off table of the sampled pixels with BOTH footprint weights
//   'PIXELS'  : 45 tasks (one per year, FIRST_YEAR..LAST_YEAR) - per-pixel daily T and Td
//   'DIAG'    : 1 task  - 12-pentad A/B/C comparison (same logic as the v02 diagnostic)
// Run WEIGHTS first, then PIXELS (optionally in batches by editing FIRST_YEAR/LAST_YEAR),
// then DIAG. Keep every exported CSV unedited and send each with its SHA-256.
//
// PER-YEAR EXTRACTION (PIXELS) is the logic of AEZ26_Eq7_PartB_PILOT_2000.js
// (pixelRows/exportPixels, same collection, bands, AOI asset, 15 km buffer, scale
// 11132 m, 0.1-degree footprint weights, calendar). Only the year loop, output
// folder, file-name prefix and the print checks are new.
//
// SET YOUR PRIVATE ASSET HERE (keep it out of anything you share):
// ============================================================================
var AOI_ASSET = 'projects/<YOUR-EE-PROJECT>/assets/<YOUR-AEZ26-ASSET>';
var ERA5_SCALE = 11132;
var DRIVE_FOLDER = 'AEZ26_Eq7_FullRecord_1981_2025';   // NEW folder; never the canonical one
var RUN_PART = 'WEIGHTS';       // 'WEIGHTS' | 'PIXELS' | 'DIAG'
var FIRST_YEAR = 1981;          // PIXELS only
var LAST_YEAR = 2025;           // PIXELS only
var PIXEL_PREFIX = 'AEZ26_Eq7FR_Pixel_T_Td_';

var aoiFC = ee.FeatureCollection(AOI_ASSET);
var aoi = aoiFC.geometry();
var eraRaw = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR');
var proj = eraRaw.first().projection();
var region = aoi.buffer(15000);

print('Run mode:', RUN_PART);
print('AOI area (km2), recorded value 1545.55:', aoi.area(1).divide(1e6));
print('Native CRS:', proj.crs(), ' nominal scale (m):', proj.nominalScale());
print('Collection first/last image dates:',
  ee.Date(eraRaw.first().get('system:time_start')).format('YYYY-MM-dd'),
  ee.Date(eraRaw.sort('system:time_start', false).first().get('system:time_start')).format('YYYY-MM-dd'));

// ---------------------------------------------------------------------------
// Shared helpers (identical to the Phase 7A / pilot definitions)
// ---------------------------------------------------------------------------
function isLeapYearJS(y) { return (y % 4 === 0) && ((y % 100 !== 0) || (y % 400 === 0)); }

// pixel rows for one daily image (IDENTICAL to the pilot's pixelRows)
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

// ---------------------------------------------------------------------------
// RUN_PART = 'WEIGHTS'  (one task)
// One row per sampled pixel with the pilot weight (footprint centred on the SAMPLED
// point, which lies about 0.0012 deg E and 0.0003 deg S of the true cell centre)
// and the weight of the TRUE native cell (centre snapped to the 0.1-deg grid).
// ---------------------------------------------------------------------------
if (RUN_PART === 'WEIGHTS') {
  var firstImg = eraRaw.first().select(['temperature_2m']);
  var samp = firstImg.sample({region: region, projection: proj, scale: ERA5_SCALE,
                              geometries: true, dropNulls: false});
  var wtab = samp.map(function (f) {
    var c = f.geometry().coordinates();
    var lon = ee.Number(c.get(0)), lat = ee.Number(c.get(1));
    var rectS = ee.Geometry.Rectangle([lon.subtract(0.05), lat.subtract(0.05),
                                       lon.add(0.05), lat.add(0.05)], null, false);
    var wS = rectS.intersection(aoi, ee.ErrorMargin(1)).area(1).divide(rectS.area(1));
    var lonN = lon.multiply(10).round().divide(10);
    var latN = lat.multiply(10).round().divide(10);
    var rectN = ee.Geometry.Rectangle([lonN.subtract(0.05), latN.subtract(0.05),
                                       lonN.add(0.05), latN.add(0.05)], null, false);
    var wN = rectN.intersection(aoi, ee.ErrorMargin(1)).area(1).divide(rectN.area(1));
    return ee.Feature(null, {
      pixel_id: lon.format('%.2f').cat('_').cat(lat.format('%.2f')),
      lon_sample: lon, lat_sample: lat, lon_native: lonN, lat_native: latN,
      coverage_weight_sample: wS, coverage_weight_native: wN});
  }).filter(ee.Filter.or(ee.Filter.gt('coverage_weight_sample', 0),
                         ee.Filter.gt('coverage_weight_native', 0)));
  print('Pixels with either weight > 0 (expect 31 or 32):', wtab.size());
  print('Sum of sample weights / native weights x ~11.1 km x 10.1 km ~ AOI area:',
        wtab.aggregate_sum('coverage_weight_sample'), wtab.aggregate_sum('coverage_weight_native'));
  Export.table.toDrive({collection: wtab, description: 'AEZ26_Eq7FR_Pixel_Weights',
    folder: DRIVE_FOLDER, fileNamePrefix: 'AEZ26_Eq7FR_Pixel_Weights', fileFormat: 'CSV',
    selectors: ['pixel_id', 'lon_sample', 'lat_sample', 'lon_native', 'lat_native',
                'coverage_weight_sample', 'coverage_weight_native']});
  print('WEIGHTS: 1 export task queued.');
}

// ---------------------------------------------------------------------------
// RUN_PART = 'PIXELS'  (one task per year)
// ---------------------------------------------------------------------------
function exportPixels(y) {
  var fc = eraRaw.filterDate(y + '-01-01', (y + 1) + '-01-01')
    .map(pixelRows).flatten();
  var name = PIXEL_PREFIX + y;
  Export.table.toDrive({collection: fc, description: name, folder: DRIVE_FOLDER,
    fileNamePrefix: name, fileFormat: 'CSV',
    selectors: ['date', 'pixel_id', 'lon', 'lat', 'coverage_weight',
                'temperature_2m_K', 'dewpoint_temperature_2m_K']});
}
if (RUN_PART === 'PIXELS') {
  for (var y = FIRST_YEAR; y <= LAST_YEAR; y++) {
    var nExpected = isLeapYearJS(y) ? 366 : 365;
    print('Year', y, '| daily images (expect ' + nExpected + '):',
      eraRaw.filterDate(y + '-01-01', (y + 1) + '-01-01').size());
    exportPixels(y);
  }
  print('PIXELS: ' + (LAST_YEAR - FIRST_YEAR + 1) + ' export tasks queued (one per year). Run each from the Tasks tab.');
  print('Check on the first day: pixels with coverage_weight > 0 (expect 31):',
    pixelRows(eraRaw.filterDate(FIRST_YEAR + '-01-01', FIRST_YEAR + '-01-02').first()).size());
}

// ---------------------------------------------------------------------------
// RUN_PART = 'DIAG'  (one task, 12 rows)
// Same pentad calendar and three reduction pathways as
// AEZ26_Eq7_Temporal_Robustness_DIAGNOSTIC_v02 (A archived scale-based composite
// reduction; B explicit native grid; C reprojection to the native grid then reduction).
// ---------------------------------------------------------------------------
var NATIVE_CRS = 'EPSG:4326';
var NATIVE_TRANSFORM = [0.1, 0, -180.05, 0, -0.1, 90.05];
var PENTADS = [
  {y:1982, p:33, stratum:'1981_1999_Jun'}, {y:1985, p:40, stratum:'1981_1999_Jul'},
  {y:1991, p:64, stratum:'1981_1999_Nov'}, {y:1997, p:70, stratum:'1981_1999_Dec'},
  {y:2001, p:46, stratum:'2000_2010_Aug'}, {y:2004, p:36, stratum:'2000_2010_Jun_leap'},
  {y:2007, p:65, stratum:'2000_2010_Nov'}, {y:2009, p:71, stratum:'2000_2010_Dec'},
  {y:2015, p:41, stratum:'2011_2025_Jul'}, {y:2018, p:47, stratum:'2011_2025_Aug'},
  {y:2020, p:66, stratum:'2011_2025_Nov_leap'}, {y:2025, p:34, stratum:'2011_2025_Jun'}
];
function pentadWindowJS(y, p) {
  var leap = isLeapYearJS(y);
  var shift = (leap && p >= 13) ? 1 : 0;
  var nDays = (leap && p === 12) ? 6 : 5;
  var start = ee.Date.fromYMD(y, 1, 1).advance((p - 1) * 5 + shift, 'day');
  return {start: start, end: start.advance(nDays, 'day'), nDays: nDays};
}
function buildComposite(y, p) {
  var w = pentadWindowJS(y, p);
  var collection = eraRaw.filterDate(w.start, w.end);
  var daily = collection.map(function (img) {
    var tC = img.select('temperature_2m').subtract(273.15);
    var tdC = img.select('dewpoint_temperature_2m').subtract(273.15);
    var es = tC.expression('0.6108 * exp((17.27 * T) / (T + 237.3))', {T: tC});
    var ea = tdC.expression('0.6108 * exp((17.27 * Td) / (Td + 237.3))', {Td: tdC});
    var rh = ea.divide(es).multiply(100).clamp(0, 100).rename('RH');
    var vpd = es.subtract(ea).max(ee.Image.constant(0)).rename('VPD');
    return ee.Image.cat([rh, vpd]).copyProperties(img, ['system:time_start']);
  });
  var temperature = collection.select('temperature_2m').mean().subtract(273.15).rename('t2m_C');
  var dewpoint = collection.select('dewpoint_temperature_2m').mean().subtract(273.15).rename('td_C');
  var rhPentad = daily.select('RH').mean().rename('RH');
  var vpdMean = daily.select('VPD').mean().rename('VPD_mean');
  var vpdMax = daily.select('VPD').max().rename('VPD_max');
  var sm1 = collection.select('volumetric_soil_water_layer_1').mean().multiply(70);
  var sm2 = collection.select('volumetric_soil_water_layer_2').mean().multiply(210);
  var sm3 = collection.select('volumetric_soil_water_layer_3').mean().multiply(720);
  var soilWater = sm1.add(sm2).add(sm3).rename('SM_mm');
  return ee.Image.cat([temperature, dewpoint, rhPentad, vpdMean, vpdMax, soilWater]);
}
function reducePathway(img, method) {
  var image = img;
  var mask = img.select('t2m_C').mask().rename('n');
  var args = {reducer: ee.Reducer.mean(), geometry: aoi, maxPixels: 1e8, tileScale: 4};
  var countArgs = {reducer: ee.Reducer.sum().combine(ee.Reducer.count(), '', true),
                   geometry: aoi, maxPixels: 1e8, tileScale: 4};
  if (method === 'A') { args.scale = ERA5_SCALE; countArgs.scale = ERA5_SCALE; }
  if (method === 'B') {
    args.crs = NATIVE_CRS; args.crsTransform = NATIVE_TRANSFORM;
    countArgs.crs = NATIVE_CRS; countArgs.crsTransform = NATIVE_TRANSFORM;
  }
  if (method === 'C') {
    image = img.reproject({crs: NATIVE_CRS, crsTransform: NATIVE_TRANSFORM});
    mask = image.select('t2m_C').mask().rename('n');
    args.crs = NATIVE_CRS; args.crsTransform = NATIVE_TRANSFORM;
    countArgs.crs = NATIVE_CRS; countArgs.crsTransform = NATIVE_TRANSFORM;
  }
  return {stats: image.reduceRegion(args), coverage: mask.reduceRegion(countArgs)};
}
function processPentad(item) {
  var w = pentadWindowJS(item.y, item.p);
  var img = buildComposite(item.y, item.p);
  var props = {
    year: item.y, pentad_of_year: item.p, stratum: item.stratum,
    pentad_start: w.start.format('YYYY-MM-dd'),
    pentad_end: w.end.advance(-1, 'day').format('YYYY-MM-dd'),
    n_days: w.nDays, era5_images: eraRaw.filterDate(w.start, w.end).size()};
  ['A', 'B', 'C'].forEach(function (m) {
    var r = reducePathway(img, m);
    props[m + '_t2m_C'] = r.stats.get('t2m_C');
    props[m + '_td_C'] = r.stats.get('td_C');
    props[m + '_RH_pct'] = r.stats.get('RH');
    props[m + '_VPD_mean_kPa'] = r.stats.get('VPD_mean');
    props[m + '_VPD_max_kPa'] = r.stats.get('VPD_max');
    props[m + '_SM_0_100_mm'] = r.stats.get('SM_mm');
    props[m + '_n_sum'] = r.coverage.get('n_sum');
    props[m + '_n_count'] = r.coverage.get('n_count');
  });
  return ee.Feature(null, props);
}
if (RUN_PART === 'DIAG') {
  var results = ee.FeatureCollection(PENTADS.map(processPentad));
  print('DIAG: total pentads (expect 12):', results.size());
  print('DIAG: first feature:', results.first());
  var columns = ['year', 'pentad_of_year', 'stratum', 'pentad_start', 'pentad_end', 'n_days', 'era5_images'];
  ['A', 'B', 'C'].forEach(function (m) {
    ['t2m_C', 'td_C', 'RH_pct', 'VPD_mean_kPa', 'VPD_max_kPa', 'SM_0_100_mm', 'n_sum', 'n_count']
      .forEach(function (v) { columns.push(m + '_' + v); });
  });
  Export.table.toDrive({collection: results, description: 'AEZ26_Eq7FR_ABC_12pentads',
    folder: DRIVE_FOLDER, fileNamePrefix: 'AEZ26_Eq7FR_ABC_12pentads', fileFormat: 'CSV',
    selectors: columns});
  print('DIAG: 1 export task queued (12 rows).');
}
