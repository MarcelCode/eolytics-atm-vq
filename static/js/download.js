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

// Draw AOI
async function add_union_layer(aoi) {
    try {
        let data = JSON.stringify(aoi.toGeoJSON().geometry);
        const union_data = await axios.get('/geodata/aoi-union/', {
            params: {
                aoi: data
            }
        });
        if (union_data.data.status === false) {
            Swal.fire({
                type: 'error',
                title: union_data.data.title,
                text: union_data.data.message,
            })
        } else {
            let geo_region = L.geoJSON(JSON.parse(union_data.data));
            drawnItems.addLayer(geo_region);
            let layer_bounds = geo_region.getBounds();
            $("#coord-ulx").text(layer_bounds._southWest.lng);
            $("#coord-uly").text(layer_bounds._northEast.lat);
            $("#coord-lrx").text(layer_bounds._northEast.lng);
            $("#coord-lry").text(layer_bounds._southWest.lat);
        }
    } catch (e) {
        console.error(e);
    }
}

let drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);
let drawControl = new L.Control.Draw({
    draw: {
        polygon: false,
        marker: false,
        circle: false,
        polyline: false,
        circlemarker: false
    },
    edit: {
        featureGroup: drawnItems,
        edit: false
    }
});
map.addControl(drawControl);

map.on("draw:created", function (e) {
    drawnItems.clearLayers();
    let layer = e.layer;
    add_union_layer(layer);
});

map.on("draw:deleted", function (e) {
    drawnItems.clearLayers();
});
// JSON.stringify(test.toGeoJSON())


// Add Geodata to map

const getGeoData = async () => {
    try {
        return await axios.get('/geodata/user-data')
    } catch (error) {
        console.error(error)
    }
};

const addGeoData = async () => {
    let json_geodata = await getGeoData();

    let geo_region = L.geoJSON(JSON.parse(json_geodata.data), {style: orange_style}).addTo(map);
    map.fitBounds(geo_region.getBounds());
    control_layer.addOverlay(geo_region, "Allowed download region");
};

addGeoData();


// GeoSearch
var GeoSearchControl = window.GeoSearch.GeoSearchControl;
var OpenStreetMapProvider = window.GeoSearch.OpenStreetMapProvider;
var provider = new OpenStreetMapProvider();

var searchControl = new GeoSearchControl({
    provider: provider,
    position: "topright"
});

map.addControl(searchControl);


// Download data
$("#download-form-button").click(function () {
    if (drawnItems.getLayers().length === 0) {
        Swal.fire({type: 'error', title: "Area of Interest is not defined!", text: "See section 1."})
    } else if ($("#startDate").val() === "") {
        Swal.fire({type: 'error', title: "Start date is not defined!", text: "See section 2."})
    } else {
        let layer_bounds = drawnItems.getLayers()[0].getBounds();
        let ulx = layer_bounds._southWest.lng;
        let uly = layer_bounds._northEast.lat;
        let lrx = layer_bounds._northEast.lng;
        let lry = layer_bounds._southWest.lat;
        let start_date = $("#startDate").val();
        let end_date = $("#endDate").val();
        if (end_date === "") {
            let d = new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate());
            end_date = (d.getMonth() + 1) + "/" + d.getDate() + "/" + d.getFullYear();
        }
        let future_download = $("#future_download").prop("checked");
        let cloud_cover = $("#cloud-range").val();

        axios.post('/geodata/start-download/', {
            user_project_pk: user_project_pk,
            ulx: ulx,
            uly: uly,
            lrx: lrx,
            lry: lry,
            start_date: start_date,
            end_date: end_date,
            cloud_cover: cloud_cover,
            future_download: future_download
        })
            .then(function (response) {
                Swal.fire({
                    type: response.data.title,
                    title: response.data.title,
                    text: response.data.message,
                })
            })
    }
});