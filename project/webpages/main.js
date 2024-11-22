import { initDom } from './utils.js';
import { baseMapInfos } from './baseMaps.js';
import { initCanvasLayer } from './canvaslayer.js';
import { getBaseMap } from './utils.js';
import { initGeoJsonLayer } from './geojsonlayer.js';

initDom(document.getElementById('map')); // set the map size to the screen size

let map = L.map('map',
    {
        renderer: L.canvas(),
    }
    // 上海经纬度：31.2304, 121.4737
).setView([31.2304, 121.4737], 11); // set the initial map view to Shanghai

let baseMaps = getBaseMap(baseMapInfos);
let layerControl = L.control.layers(baseMaps).addTo(map);
baseMaps["dark_all"].addTo(map);

initCanvasLayer();
initGeoJsonLayer();

const infoUpdate = function (props) {
    // const contents = props ? `<b>${props.Shape_Leng}</b><br />${props.COUNT_} people` : 'Hover over a state';
    const contents = props ? `<b>length : ${props.Shape_Leng}</b><br/> trajectory count : ${props.COUNT_} ` : 'Hover over a trajectory';
    this._div.innerHTML = `${contents}`;
}

const infoUpdate2 = function (props) {
    // const contents = props ? `<b>${props.Shape_Leng}</b><br />${props.COUNT_} people` : 'Hover over a state';
    const contents = props ? `<b>RoadID : ${props.RoadID}</b><br/> trajectory count : ${props.MEAN_Tree} ` : 'Hover over a trajectory';
    this._div.innerHTML = `${contents}`;
}

const geoJsonLayer = L.geoJsonLayer(infoUpdate);
const geoJsonLayer2 = L.geoJsonLayer(infoUpdate2);

layerControl.addOverlay(geoJsonLayer, 'trajectory');
layerControl.addOverlay(geoJsonLayer2, 'streetscapeIndex');

// geoJsonLayer.addTo(map);
geoJsonLayer2.addTo(map);

// 获取 CSV 文件并解析为数组
fetch('../data/8.1-7.geojson')
    .then(response => response.json())
    .then(data => {
        // geoJsonLayer.updateData(toGeoJson(hull));
        geoJsonLayer.updateData(data, (d) => parseInt(d.properties.COUNT_));
    })
    .catch(error => {
        console.error('Error:', error);
});

// project\data\streetscapeIndex.geojson

fetch('../data/streetscapeIndex.geojson')
    .then(response => response.json())
    .then(data => {
        // console.log(data)
        // 只显示前1000条数据
        // data.features = data.features.slice(0, 1000);
        // console.log(data)
        geoJsonLayer2.updateData(data, (d) => parseInt(d.properties.MEAN_Build));
    })
    .catch(error => {
        console.error('Error:', error);
    });

