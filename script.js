var view;
require([
  'esri/layers/FeatureLayer',
  'esri/layers/TileLayer',
  'esri/Map',
  'esri/renderers/SimpleRenderer',
  'esri/symbols/ExtrudeSymbol3DLayer',
  'esri/symbols/PolygonSymbol3D',
  'esri/views/SceneView',
  'esri/layers/GraphicsLayer',
  'esri/symbols/SimpleMarkerSymbol',

  'esri/Graphic',
  'esri/geometry/Point',

  'esri/widgets/Home',

  'dojo/domReady!'
], function(
  FeatureLayer, TileLayer, Map, SimpleRenderer, ExtrudeSymbol3DLayer, PolygonSymbol3D, SceneView, GraphicsLayer, SimpleMarkerSymbol, Graphic, Point, Home
) {

  /*var basketballCourtMapServiceUrl =
    '//tiles.arcgis.com/tiles/g2TonOxuRkIqSOFx/arcgis/rest/services/BW_Court_Tiles/MapServer';*/
  var basketballCourtMapServiceUrl =
    '//tiles.arcgis.com/tiles/g2TonOxuRkIqSOFx/arcgis/rest/services/Dark_Basketball_Court/MapServer';
  var hexbinsFeatureServiceUrl =
    '//services1.arcgis.com/g2TonOxuRkIqSOFx/arcgis/rest/services/KD_RegSeason_2015_16/FeatureServer/1';
  //'//services1.arcgis.com/g2TonOxuRkIqSOFx/arcgis/rest/services/Scene_NBA_Test2_WFL/FeatureServer/0';
  var missesFeatureServiceUrl =
    '//services1.arcgis.com/g2TonOxuRkIqSOFx/arcgis/rest/services/KD_RegSeason_2015_16/FeatureServer/0';
  //'//services1.arcgis.com/g2TonOxuRkIqSOFx/arcgis/rest/services/Scene_NBA_Test2_WFL/FeatureServer/0';

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
        color: [204, 204, 255, 255],
      }, {
        value: 2,
        color: [167, 150, 250, 255],
      }, {
        value: 4,
        color: [126, 99, 242, 255],
      }, {
        value: 8,
        color: [81, 54, 235, 255],
      }, {
        value: 14,
        color: [0, 0, 224, 255],
      }]
    }]
  });

  var missesRenderer = new SimpleRenderer({
    symbol: new PolygonSymbol3D({
      symbolLayers: [new ExtrudeSymbol3DLayer()]
    }),
    visualVariables: [{
      type: 'size',
      field: 'Point_Count',
      stops: [{
        value: 1,
        size: -10,
      }, {
        value: 2,
        size: -20,
      }, {
        value: 3,
        size: -30,
      }, {
        value: 4,
        size: -40,
      }, {
        value: 6,
        size: -60,
      }, {
        value: 8,
        size: -80,
      }]
    }, {
      type: 'color',
      field: 'Point_Count',
      stops: [{
        value: 1,
        color: [255, 204, 204, 255],
      }, {
        value: 2,
        color: [255, 158, 143, 255],
      }, {
        value: 3,
        color: [250, 114, 90, 255],
      }, {
        value: 4,
        color: [237, 67, 45, 255],
      }, {
        value: 6,
        color: [219, 0, 0, 255],
      }]
    }]
  });

  var featureLayer = new FeatureLayer({
    url: hexbinsFeatureServiceUrl,
    renderer: renderer,
    mode: FeatureLayer.MODE_SNAPSHOT,
    elevationInfo: {
      mode: 'relative-to-ground',
      offset: 3.0
    }
  });

  var missesFeatureLayer = new FeatureLayer({
    url: missesFeatureServiceUrl,
    renderer: missesRenderer,
    mode: FeatureLayer.MODE_SNAPSHOT,
    elevationInfo: {
      mode: 'relative-to-ground', //'on-the-ground'
      offset: -3.0
    }
  });

  //-------------
  var graphicsLayer = new GraphicsLayer();


  /*************************
   * Add a 3D point graphic
   *************************/

  // London
  var point = new Point({
      x: 0,
      y: 47,
      z: 10
    }),

    markerSymbol = new SimpleMarkerSymbol({
      color: [226, 119, 40],

      outline: { // autocasts as new SimpleLineSymbol()
        color: [255, 255, 255],
        width: 10
      }
    });

  var pointGraphic = new Graphic({
    geometry: point,
    symbol: markerSymbol
  });

  graphicsLayer.add(pointGraphic);
  //map.add(graphicsLayer);
  //-----

  //tileLayer.opacity = 0.5;
  var map = new Map({
    // basemap: 'topo',
    layers: [tileLayer, featureLayer, missesFeatureLayer, graphicsLayer]
  });

  view = new SceneView({
    container: 'viewDiv',
    map: map,
    viewingMode: 'local',
    constraints: {
      collision: {
        enabled: false
      },
      tilt: {
        max: 180
      }
    },
    camera: {
      position: {
        x: 0,
        y: 0,
        z: 500
      },
      heading: 270,
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

    var homeBtn = new Home({
      view: view
    }, 'homeDiv');
    homeBtn.startup();
    view.ui.add(homeBtn, 'top-left');

    var hitsCameraBtn = document.getElementById('hitsCameraBtn');
    var compareCameraBtn = document.getElementById('compareCameraBtn');
    var missesCameraBtn = document.getElementById('missesCameraBtn');

    [hitsCameraBtn, compareCameraBtn, missesCameraBtn].forEach(function(button) {
      button.style.display = 'flex';
      view.ui.add(button, 'top-right');
    });

    hitsCameraBtn.addEventListener('click', function() {
      // reuse the default camera position already established in the homeBtn
      view.goTo({
        position: {
          x: 0,
          y: 0,
          z: 1200
        },
        tilt: 0,
        heading: 270
      });
    });

    compareCameraBtn.addEventListener('click', function() {
      view.goTo({
        position: {
          latitude: 0.0037504663085195862,
          longitude: 0.01260657228669327,
          z: 0
        },
        tilt: 90,
        heading: 270
      });
    });

    missesCameraBtn.addEventListener('click', function() {
      view.goTo({
        position: {
          x: 0,
          y: 0,
          z: -1000
        },
        tilt: 180,
        heading: 270
      });
    });

  });

});
