// Rafael Rossi Viégas 
// rafarviegas@gmail.com 
// rafael@canopyrss.tech
// +55 (54)996495269
// 04/05/2018 ~ v02

/////////////////////////////////////////////////////////////////////////

// user input

var ft = 0;

var start_date = '2017-01-01';
var end_date =  '2017-12-10';

// enable (I)
var path = 216;
var row = 73;

// enable (II)
var tile = '23MKQ';

// enable (III)
var roi = ee.FeatureCollection('users/rafarviegas/roi_bbox')

/////////////////////////////////////////////////////////////////////////
// doing some stuff so it all works in the end, or at least it should

// loading image collections and selecting only the necessary bands
// note that the values for all collections are already 
// scalled between 0 and 10000
var collection_landsat_5 = ee.ImageCollection('LANDSAT/LT05/C01/T1_SR')
      .select(['B4', 'B5', 'B3'], ['nir', 'swir', 'red']);
var collection_landsat_7 = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR')
      .select(['B4', 'B5', 'B3'], ['nir', 'swir', 'red']);
var collection_landsat_8 = ee.ImageCollection('LANDSAT/LC08/C01/T1_SR')
      .select(['B5', 'B6', 'B4'], ['nir', 'swir', 'red']);
var collection_sentinel_2 = ee.ImageCollection('COPERNICUS/S2')
      .select(['B8A', 'B11', 'B4'], ['nir', 'swir', 'red']);


// merge collections, now that they are all 'alike'
var collection = ee.ImageCollection(
      collection_landsat_5
      .merge(collection_landsat_7)
      .merge(collection_landsat_8)
      .merge(collection_sentinel_2)
    );

// (I) path row filter, works only for landsat 
// collection = collection.filterMetadata('WRS_PATH', 'equals', path)
//   .filterMetadata("WRS_ROW", 'equals', row);

// (II) mgrs tile filter, works only for sentinel 
collection = collection.filterMetadata('MGRS_TILE', 'equals', path);

// (III) filter by a given roi, works for both satellites
// collection = collection.filterBounds(roi);


// filtering collection
// -> looking only for the images(/featues) in the specified period of time
collection = collection.filterDate(start_date, end_date);

print(collection);
// sorting collection by image acquisition date 
collection = collection.sort('system:time_start');

// bringing home the needed information
var collection_list = collection.toList(5000);
var collection_info = collection_list.getInfo();

// diplaying images 
var vis_params = {'min':0, 'max':4250, 'gamma':1.2};
for (var i = 0; i < collection_info.length; i++) {
  var img = ee.Image(collection_list.get(i));
  Map.addLayer(img, vis_params, collection_info[i].id, false);
}



// OBS 1: Os dados utilizados sao 
// reflectancia da superficie: Landsats 5,7 e 8 
// reflectancia no topo da atmosfera para o Sentinel 2 

// OBS 2: Este script teoricamente funciona para qualquer janela temporal, 
// desde que ela compreenda no máximo 5k imagens - ver linha 50,
// entretanto prefira janelas pequenas a janelas grande a experencia do 
// usuario sera bem melhor e a chance travar o navegador eh bem menor 
