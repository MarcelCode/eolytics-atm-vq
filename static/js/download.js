let orange_style = {
    "color": "#ff8702",
    "weight": 1,
    "opacity": 0.5
};

let blue_style = {
    "color": "#25488a",
    "weight": 1,
    "opacity": 0.5
};

// Main map
var map = L.map('map', {maxZoom: 17, zoomControl: false}).setView([15, 0], 3);

baselayers = {
    ocean_layer: L.layerGroup([L.esri.basemapLayer("Oceans"), L.esri.basemapLayer('OceansLabels')]),
    image_layer: L.esri.basemapLayer("Imagery"),
    topo_layer: L.esri.basemapLayer("Topographic")
};

map.addLayer(baselayers.image_layer);

var baselayer_label = {
    "Esri Oceans": baselayers.ocean_layer,
    "Esri Imagery": baselayers.image_layer,
    "Esri Topographic": baselayers.topo_layer
};

var control_layer = L.control.layers(baselayer_label).addTo(map);

L.control.zoom({
    position: 'topright'
}).addTo(map);


let geo_region = L.geoJSON(geodata, {style: orange_style}).addTo(map);

map.fitBounds(geo_region.getBounds());

control_layer.addOverlay(geo_region, "Landsat 8 Scenes");


// GeoSearch
var GeoSearchControl = window.GeoSearch.GeoSearchControl;
var OpenStreetMapProvider = window.GeoSearch.OpenStreetMapProvider;
var provider = new OpenStreetMapProvider();

var searchControl = new GeoSearchControl({
    provider: provider,
    position: "topright"
});

map.addControl(searchControl);


// layer on click
geo_region.on("click", function (e) {
    test = e;
    if (e.layer.options.color === orange_style.color){
        e.layer.setStyle(blue_style);
    }
    else {
        e.layer.setStyle(orange_style);
    }

});