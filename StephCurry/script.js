var view;
require([
  'esri/layers/FeatureLayer',
  'esri/layers/TileLayer',
  'esri/Map',
  'esri/renderers/SimpleRenderer',
  'esri/symbols/ExtrudeSymbol3DLayer',
  'esri/symbols/PolygonSymbol3D',
  'esri/views/SceneView',
  'esri/widgets/Home',
  'esri/tasks/support/Query',

  'dojo/domReady!'
], function(
  FeatureLayer, TileLayer, Map, SimpleRenderer, ExtrudeSymbol3DLayer, PolygonSymbol3D, SceneView, Home, Query
) {



  /*var basketballCourtMapServiceUrl =
    '//tiles.arcgis.com/tiles/g2TonOxuRkIqSOFx/arcgis/rest/services/BW_Court_Tiles/MapServer';*/
  var basketballCourtMapServiceUrl =
    '//tiles.arcgis.com/tiles/g2TonOxuRkIqSOFx/arcgis/rest/services/Dark_Basketball_Court/MapServer';
  var hexbinsFeatureServiceUrl =
    '//services1.arcgis.com/g2TonOxuRkIqSOFx/arcgis/rest/services/StephCurry_2016_17_WFL1/FeatureServer/0';
  /*'//services1.arcgis.com/g2TonOxuRkIqSOFx/arcgis/rest/services/Scene_NBA_Test2_WFL/FeatureServer/0';
   */
  var tileLayer = new TileLayer({
    url: basketballCourtMapServiceUrl
  });

  var renderer = new SimpleRenderer({
    symbol: new PolygonSymbol3D({
      symbolLayers: [new ExtrudeSymbol3DLayer()]
    }),
    visualVariables: [{
      type: 'size',
      field: 'Point_Count',
      stops: [{
        value: 1,
        size: 10,
      }, {
        value: 2,
        size: 20,
      }, {
        value: 4,
        size: 40,
      }, {
        value: 8,
        size: 80,
      }, {
        value: 14,
        size: 140,
      }, {
        value: 24,
        size: 240,
      }]
    }, {
      type: 'color',
      field: 'Point_Count',
      stops: [{
        value: 1,
        color: [212, 227, 245, 255],
      }, {
        value: 2,
        color: [133, 154, 250, 255],
      }, {
        value: 4,
        color: [62, 90, 253, 255],
      }, {
        value: 8,
        color: [10, 42, 244, 255],
      }, {
        value: 14,
        color: [132, 149, 122, 255],
      }, {
        value: 24,
        color: [255, 255, 0, 255],
      }]
    }]
  });

  var featureLayer = new FeatureLayer({
    url: hexbinsFeatureServiceUrl,
    definitionExpression: "GAME_DATE='2016-10-28'",
    renderer: renderer
  });

  var map = new Map({
    // basemap: 'topo',
    layers: [tileLayer, featureLayer]
  });

  view = new SceneView({
    container: 'viewDiv',
    map: map,
    viewingMode: 'local',
    camera: {
      position: {
        x: 0,
        y: 0,
        z: 750
      },
      heading: -90,
      tilt: 45
    },
    environment: {
      atmosphere: null,
      starsEnabled: false
    }
  });

  view.then(function() {
    // Use the exent defined in clippingArea to define the bounds of the scene
    view.clippingArea = tileLayer.fullExtent;
    view.extent = tileLayer.fullExtent;

    featureLayer.then(function() {
      var query = new Query();
      query.where = "1=1";
      query.returnGeometry = false;
      query.outFields = ["GAME_DATE"];
      query.orderByFields = ["GAME_DATE ASC"];
      query.returnDistinctValues = true;

      // Queries for all the features in the service (not the graphics in the view)
      featureLayer.queryFeatures(query).then(function(results) {
        // prints an array of all the features in the service to the console
        console.log(results.features);

        var uniqueDates = results.features.map(function(feature) {
          return new Date(feature.attributes.GAME_DATE).toJSON().split('T')[0];
        });

        var gameDateSlider = document.getElementById('gameDateSlider');
        var dateLabel = document.getElementById('dateLabel');

        dateLabel.innerHTML = uniqueDates[0];

        gameDateSlider.addEventListener('change', function(evt) {
          var dataIndex = evt.target.value;
          console.log(dataIndex);


          dateLabel.innerHTML = uniqueDates[dataIndex];
          var newExpression = 'GAME_DATE = \'' + uniqueDates[dataIndex] + '\'';
          featureLayer.definitionExpression = newExpression;
        });

      });

    });

  });

  var homeBtn = new Home({
    view: view
  }, 'homeDiv');
  view.ui.add(homeBtn, 'top-left');

});