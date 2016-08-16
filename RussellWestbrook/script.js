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

  "esri/PopupTemplate",

  'esri/widgets/Home',

  'dojo/domReady!'
], function(
  FeatureLayer, TileLayer, Map, SimpleRenderer, ExtrudeSymbol3DLayer, PolygonSymbol3D, SceneView, GraphicsLayer, SimpleMarkerSymbol, Graphic, Point, PopupTemplate, Home
) {

  /*var basketballCourtMapServiceUrl =
    '//tiles.arcgis.com/tiles/g2TonOxuRkIqSOFx/arcgis/rest/services/BW_Court_Tiles/MapServer';*/
  var basketballCourtMapServiceUrl =
    '//tiles.arcgis.com/tiles/g2TonOxuRkIqSOFx/arcgis/rest/services/Dark_Basketball_Court/MapServer';
    //'http://tiles.arcgis.com/tiles/g2TonOxuRkIqSOFx/arcgis/rest/services/White_Basketball_Court/MapServer';
  var rwMakesFeatureServiceUrl =
    '//services1.arcgis.com/g2TonOxuRkIqSOFx/arcgis/rest/services/KD_RegSeason_2015_16/FeatureServer/1';
  //'//services1.arcgis.com/g2TonOxuRkIqSOFx/arcgis/rest/services/Scene_NBA_Test2_WFL/FeatureServer/0';
  var rwMissesFeatureServiceUrl =
    '//services1.arcgis.com/g2TonOxuRkIqSOFx/arcgis/rest/services/KD_RegSeason_2015_16/FeatureServer/0';
  //'//services1.arcgis.com/g2TonOxuRkIqSOFx/arcgis/rest/services/Scene_NBA_Test2_WFL/FeatureServer/0';
  var hexbinsFeatureServiceUrl =
    'http://services1.arcgis.com/g2TonOxuRkIqSOFx/arcgis/rest/services/Thunder_Shots_Hexbins/FeatureServer/7';  
  var missesFeatureServiceUrl =
    'http://services1.arcgis.com/g2TonOxuRkIqSOFx/arcgis/rest/services/Thunder_Shots_Hexbins/FeatureServer/6';
    
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
        value: 8,
        size: 80,
      }, {
        value: 17,
        size: 170,
      }, {
        value: 29,
        size: 290,
      }, {
        value: 96,
        size: 320,
      }]
    }, {
      type: 'color',
      field: 'Point_Count',
      stops: [{
        value: 1,
        color: [247,251,255,255],
      }, {
        value: 2,
        color: [198,219,239,255],
      }, {
        value: 8,
        color: [107,174,214,255],
      }, {
        value: 17,
        color: [0,125,195,255],
      }, {
        value: 29,
        color: [0,44,98,255],
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
        value: 7,
        size: -70,
      }, {
        value: 11,
        size: -110,
      }, {
        value: 15,
        size: -150,
      }]
    }, {
      type: 'color',
      field: 'Point_Count',
      stops: [{
        value: 1,
        color: [254,240,217,255],
      }, {
        value: 2,
        color: [253,204,138,255],
      }, {
        value: 7,
        color: [252,141,89,255],
      }, {
        value: 11,
        color: [240,81,51,255],
      }, {
        value: 15,
        color: [179,0,0,255],
      }]
    }]
  });

  var made_template = new PopupTemplate({
        // ZIP is the name of a field in the service containing the zip code number of the feature
        title: "Russell Westbrook Made {Point_Count} Shots"
  });

  var miss_template = new PopupTemplate({
        // ZIP is the name of a field in the service containing the zip code number of the feature
        title: "Russell Westbrook Missed {Point_Count} Shots"
  });

  var featureLayer = new FeatureLayer({
    url: hexbinsFeatureServiceUrl,
    outFields: ["*"],
    popupTemplate: made_template,
    renderer: renderer,
    mode: FeatureLayer.MODE_SNAPSHOT,
    elevationInfo: {
      mode: 'relative-to-ground',
      offset: 2.5
    }
  });

  var missesFeatureLayer = new FeatureLayer({
    url: missesFeatureServiceUrl,
    outFields: ["*"],
    popupTemplate: miss_template,
    renderer: missesRenderer,
    mode: FeatureLayer.MODE_SNAPSHOT,
    elevationInfo: {
      mode: 'relative-to-ground', //'on-the-ground'
      offset: -2.5
    }
  });

  var rwMissesFeatureLayer = new FeatureLayer({
    url: rwMissesFeatureServiceUrl,
    renderer: missesRenderer,
    mode: FeatureLayer.MODE_SNAPSHOT,
    elevationInfo: {
      mode: 'relative-to-ground', //'on-the-ground'
      offset: -2.5
    }
  });
  
  var rwMakesFeatureLayer = new FeatureLayer({
    url: rwMakesFeatureServiceUrl,
    renderer: renderer,
    mode: FeatureLayer.MODE_SNAPSHOT,
    elevationInfo: {
      mode: 'relative-to-ground', //'on-the-ground'
      offset: 2.5
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
    layers: [tileLayer, featureLayer, missesFeatureLayer] //,rwMakesFeatureLayer,rwMissesFeatureLayer]
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
    var compareAwayBaselineCameraBtn = document.getElementById('compareAwayBaselineCameraBtn');
    var compareHomeBaselineCameraBtn = document.getElementById('compareHomeBaselineCameraBtn');
    var missesCameraBtn = document.getElementById('missesCameraBtn');

    [hitsCameraBtn, compareCameraBtn, compareAwayBaselineCameraBtn, compareHomeBaselineCameraBtn, missesCameraBtn].forEach(function(button) {
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
          x: 0.01,
          y: 0,
          z: 0
        },
        tilt: 90,
        heading: 270
      });
    });

    compareAwayBaselineCameraBtn.addEventListener('click', function() {
      view.goTo({
        position: {
          x: 0,
          y: 0.01,
          z: 0
        },
        tilt: 90,
        heading: 180
      });
    });

    compareHomeBaselineCameraBtn.addEventListener('click', function() {
      view.goTo({
        position: {
          x: 0,
          y: -0.01,
          z: 0
        },
        tilt: 90,
        heading: 0
      });
    });

    missesCameraBtn.addEventListener('click', function() {
      view.goTo({
        position: {
          x: 0,
          y: 0,
          z: -1200
        },
        tilt: 0,
        heading: 90
      });
    });

  });

});
