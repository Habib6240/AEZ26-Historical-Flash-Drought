
// ============================================================================
// AEZ-26 — EQUATION 7 TEMPORAL ROBUSTNESS DIAGNOSTIC
// Version: v02 — Numeric native transform correction
//
// PURPOSE:
// Compare three spatial-reduction pathways using 23 pre-selected pentads.
//
// A = Archived composite reduction (original scale-based method)
// B = Composite reduced using explicit native ERA5-Land grid
// C = Composite reprojected to native grid before reduction
//
// OUTPUT:
// One CSV containing 23 rows.
// No pixel-level export.
// No modification of original research data.
//
// ============================================================================


// ---------------------------------------------------------------------------
// 1. USER SETTINGS
// ---------------------------------------------------------------------------

var AOI_ASSET =
  'projects/<YOUR-EE-PROJECT>/assets/<YOUR-AEZ26-ASSET>';

var DRIVE_FOLDER = 'AEZ26_Final_Research_Data';

var SCALE = 11132;

var aoiFC = ee.FeatureCollection(AOI_ASSET);
var aoi = aoiFC.geometry();

var eraRaw = ee.ImageCollection(
  'ECMWF/ERA5_LAND/DAILY_AGGR'
);


// ---------------------------------------------------------------------------
// 2. NATIVE ERA5-LAND GRID
// ---------------------------------------------------------------------------

// Confirmed from your original GEE Console output.
// CRS: EPSG:4326
// Native resolution: approximately 11131.949 metres.
//
// IMPORTANT:
// Use a numeric JavaScript array, NOT projection.transform()
// because your previous output returned a String.

var NATIVE_CRS = 'EPSG:4326';

var NATIVE_TRANSFORM = [
  0.1, 0, -180.05,
  0, -0.1, 90.05
];

var firstImage = eraRaw.first();

var nativeProjection =
  firstImage.select('temperature_2m').projection();


// ---------------------------------------------------------------------------
// 3. PRE-SELECTED PENTADS
// ---------------------------------------------------------------------------

var PENTADS = [

  // Early period: 1981–1990
  {y:1989, p:26, stratum:'early_1981_1990'},
  {y:1986, p:55, stratum:'early_1981_1990'},
  {y:1989, p:3, stratum:'early_1981_1990'},
  {y:1988, p:12, stratum:'early_1981_1990'},
  {y:1988, p:13, stratum:'early_1981_1990'},

  // Middle period: 1991–2005
  {y:1992, p:21, stratum:'middle_1991_2005'},
  {y:2000, p:53, stratum:'middle_1991_2005'},
  {y:1993, p:5, stratum:'middle_1991_2005'},
  {y:2000, p:12, stratum:'middle_1991_2005'},
  {y:2000, p:13, stratum:'middle_1991_2005'},
  {y:2000, p:55, stratum:'middle_1991_2005'},

  // Later period: 2006–2020
  {y:2014, p:23, stratum:'later_2006_2020'},
  {y:2012, p:52, stratum:'later_2006_2020'},
  {y:2013, p:2, stratum:'later_2006_2020'},
  {y:2016, p:12, stratum:'later_2006_2020'},
  {y:2016, p:13, stratum:'later_2006_2020'},
  {y:2010, p:54, stratum:'later_2006_2020'},

  // Recent period: 2021–2025
  {y:2024, p:24, stratum:'recent_2021_2025'},
  {y:2022, p:52, stratum:'recent_2021_2025'},
  {y:2023, p:4, stratum:'recent_2021_2025'},
  {y:2024, p:12, stratum:'recent_2021_2025'},
  {y:2024, p:13, stratum:'recent_2021_2025'},
  {y:2022, p:56, stratum:'recent_2021_2025'}

];


// ---------------------------------------------------------------------------
// 4. PHASE A — AOI AND PROJECTION VALIDATION
// ---------------------------------------------------------------------------

print('========== AOI VALIDATION ==========');

print('AOI feature count:', aoiFC.size());

print('AOI area (km2):',
  aoi.area(1).divide(1e6));

print('AOI centroid:',
  aoi.centroid(1).coordinates());

print('AOI vertex count:',
  aoi.coordinates().flatten().size().divide(2));

print('Recorded AOI area: 1545.55 km2');

print('Native CRS:',
  nativeProjection.crs());

print('Native projection:',
  nativeProjection);

print('Numeric native transform:',
  NATIVE_TRANSFORM);

print('Native nominal scale:',
  nativeProjection.nominalScale());


// Inspect temporal composite projection.

var testComposite = eraRaw
  .filterDate('2000-01-01', '2000-01-06')
  .select('temperature_2m')
  .mean();

print('Composite projection:',
  testComposite.projection());

print('Composite nominal scale:',
  testComposite.projection().nominalScale());


// ---------------------------------------------------------------------------
// 5. LEAP-YEAR AND PENTAD CALENDAR
// ---------------------------------------------------------------------------

function isLeapYear(y) {

  return (y % 4 === 0) &&
    ((y % 100 !== 0) || (y % 400 === 0));

}


function pentadWindow(y, p) {

  var leap = isLeapYear(y);

  var shift = (leap && p >= 13) ? 1 : 0;

  var nDays = (leap && p === 12) ? 6 : 5;

  var start = ee.Date.fromYMD(y, 1, 1)
    .advance((p - 1) * 5 + shift, 'day');

  var end = start.advance(nDays, 'day');

  return {
    start: start,
    end: end,
    nDays: nDays
  };

}


// ---------------------------------------------------------------------------
// 6. BUILD PENTAD COMPOSITES
// ---------------------------------------------------------------------------

function buildComposite(y, p) {

  var window = pentadWindow(y, p);

  var collection = eraRaw.filterDate(
    window.start,
    window.end
  );

  // Daily thermodynamic calculations.

  var daily = collection.map(function(img) {

    var tC = img.select('temperature_2m')
      .subtract(273.15);

    var tdC = img.select('dewpoint_temperature_2m')
      .subtract(273.15);

    var es = tC.expression(
      '0.6108 * exp((17.27 * T) / (T + 237.3))',
      {T: tC}
    );

    var ea = tdC.expression(
      '0.6108 * exp((17.27 * Td) / (Td + 237.3))',
      {Td: tdC}
    );

    var rh = ea.divide(es)
      .multiply(100)
      .clamp(0, 100)
      .rename('RH');

    var vpd = es.subtract(ea)
      .max(ee.Image.constant(0))
      .rename('VPD');

    return ee.Image.cat([rh, vpd])
      .copyProperties(img, ['system:time_start']);

  });


  // Temperature and dewpoint pentad means.

  var temperature = collection
    .select('temperature_2m')
    .mean()
    .subtract(273.15)
    .rename('t2m_C');

  var dewpoint = collection
    .select('dewpoint_temperature_2m')
    .mean()
    .subtract(273.15)
    .rename('td_C');


  // Daily VPD and RH -> pentad aggregation.

  var rhPentad = daily.select('RH')
    .mean()
    .rename('RH');

  var vpdMean = daily.select('VPD')
    .mean()
    .rename('VPD_mean');

  var vpdMax = daily.select('VPD')
    .max()
    .rename('VPD_max');


  // Equation 6: ERA5-Land soil-water storage.

  var sm1 = collection
    .select('volumetric_soil_water_layer_1')
    .mean()
    .multiply(70);

  var sm2 = collection
    .select('volumetric_soil_water_layer_2')
    .mean()
    .multiply(210);

  var sm3 = collection
    .select('volumetric_soil_water_layer_3')
    .mean()
    .multiply(720);

  var soilWater = sm1.add(sm2)
    .add(sm3)
    .rename('SM_mm');


  return ee.Image.cat([
    temperature,
    dewpoint,
    rhPentad,
    vpdMean,
    vpdMax,
    soilWater
  ]);

}


// ---------------------------------------------------------------------------
// 7. THREE SPATIAL-REDUCTION PATHWAYS
// ---------------------------------------------------------------------------

function reducePathway(img, method) {

  var image = img;

  var mask = img.select('t2m_C')
    .mask()
    .rename('n');


  var args = {
    reducer: ee.Reducer.mean(),
    geometry: aoi,
    maxPixels: 1e8,
    tileScale: 4
  };


  var countArgs = {
    reducer: ee.Reducer.sum()
      .combine(ee.Reducer.count(), '', true),
    geometry: aoi,
    maxPixels: 1e8,
    tileScale: 4
  };


  // A: Original archived scale-based pathway.

  if (method === 'A') {

    args.scale = SCALE;

    countArgs.scale = SCALE;

  }


  // B: Explicit native grid.

  if (method === 'B') {

    args.crs = NATIVE_CRS;

    args.crsTransform = NATIVE_TRANSFORM;

    countArgs.crs = NATIVE_CRS;

    countArgs.crsTransform = NATIVE_TRANSFORM;

  }


  // C: Explicit reprojection followed by native-grid reduction.

  if (method === 'C') {

    image = img.reproject({
      crs: NATIVE_CRS,
      crsTransform: NATIVE_TRANSFORM
    });

    mask = image.select('t2m_C')
      .mask()
      .rename('n');

    args.crs = NATIVE_CRS;

    args.crsTransform = NATIVE_TRANSFORM;

    countArgs.crs = NATIVE_CRS;

    countArgs.crsTransform = NATIVE_TRANSFORM;

  }


  var statistics = image.reduceRegion(args);

  var coverage = mask.reduceRegion(countArgs);

  return {
    stats: statistics,
    coverage: coverage
  };

}


// ---------------------------------------------------------------------------
// 8. PROCESS EACH PRE-SELECTED PENTAD
// ---------------------------------------------------------------------------

function processPentad(item) {

  var y = item.y;

  var p = item.p;

  var window = pentadWindow(y, p);

  var img = buildComposite(y, p);


  var properties = {

    year: y,

    pentad_of_year: p,

    stratum: item.stratum,

    pentad_start: window.start.format('YYYY-MM-dd'),

    pentad_end: window.end.advance(-1, 'day')
      .format('YYYY-MM-dd'),

    n_days: window.nDays,

    era5_images: eraRaw.filterDate(
      window.start,
      window.end
    ).size()

  };


  ['A', 'B', 'C'].forEach(function(method) {

    var result = reducePathway(img, method);

    var stats = result.stats;

    var coverage = result.coverage;


    properties[method + '_t2m_C'] =
      stats.get('t2m_C');

    properties[method + '_td_C'] =
      stats.get('td_C');

    properties[method + '_RH_pct'] =
      stats.get('RH');

    properties[method + '_VPD_mean_kPa'] =
      stats.get('VPD_mean');

    properties[method + '_VPD_max_kPa'] =
      stats.get('VPD_max');

    properties[method + '_SM_0_100_mm'] =
      stats.get('SM_mm');

    properties[method + '_n_sum'] =
      coverage.get('n_sum');

    properties[method + '_n_count'] =
      coverage.get('n_count');

  });


  return ee.Feature(null, properties);

}


// ---------------------------------------------------------------------------
// 9. CREATE FINAL 23-ROW FEATURE COLLECTION
// ---------------------------------------------------------------------------

var results = ee.FeatureCollection(
  PENTADS.map(processPentad)
);

print('========== FIRST RESULT ==========');

print('First feature:', results.first());

print('Total pentads:', results.size());


// ---------------------------------------------------------------------------
// 10. CSV COLUMN SELECTION
// ---------------------------------------------------------------------------

var columns = [

  'year',
  'pentad_of_year',
  'stratum',
  'pentad_start',
  'pentad_end',
  'n_days',
  'era5_images'

];


['A', 'B', 'C'].forEach(function(method) {

  [

    't2m_C',
    'td_C',
    'RH_pct',
    'VPD_mean_kPa',
    'VPD_max_kPa',
    'SM_0_100_mm',
    'n_sum',
    'n_count'

  ].forEach(function(variable) {

    columns.push(method + '_' + variable);

  });

});


// ---------------------------------------------------------------------------
// 11. EXPORT ONE SMALL CSV
// ---------------------------------------------------------------------------

Export.table.toDrive({

  collection: results,

  description:
    'AEZ26_Eq7_Temporal_Robustness_23pentads_v02',

  folder: DRIVE_FOLDER,

  fileNamePrefix:
    'AEZ26_Eq7_Temporal_Robustness_23pentads_v02',

  fileFormat: 'CSV',

  selectors: columns

});


print('========================================');

print('DIAGNOSTIC SCRIPT COMPLETED');

print('Expected export rows: 23');

print('Export: Tasks tab -> Run');

print('No pixel-level export was created.');

print('========================================');
