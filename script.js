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

  'dojo/domReady!'
], function(
  FeatureLayer, TileLayer, Map, SimpleRenderer, ExtrudeSymbol3DLayer, PolygonSymbol3D, SceneView, Home
) {

  var basketballCourtMapServiceUrl =
    '//tiles.arcgis.com/tiles/g2TonOxuRkIqSOFx/arcgis/rest/services/BW_Court_Tiles/MapServer';
  var hexbinsFeatureServiceUrl =
    '//services1.arcgis.com/g2TonOxuRkIqSOFx/arcgis/rest/services/Scene_NBA_Test2_WFL/FeatureServer/0';

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
        value: 20,
        size: 100,
      }, {
        value: 80,
        size: 100,
      }, {
        value: 140,
        size: 100,
      }, {
        value: 240,
        size: 100,
      }]
    }, {
      type: 'color',
      field: 'Point_Count',
      stops: [{
        value: 1,
        color: '#FFFCD4',
      }, {
        value: 10,
        color: [153, 83, 41],
      }]
    }]
  });

  var featureLayer = new FeatureLayer({
    url: hexbinsFeatureServiceUrl,
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
        y: 0
      },
      heading: 90,
      tilt: 0
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
  });

  var homeBtn = new Home({
    view: view
  }, 'homeDiv');
  homeBtn.startup();
  view.ui.add(homeBtn, 'top-left');
});
