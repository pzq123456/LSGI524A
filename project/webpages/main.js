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

const geoJsonLayer = L.geoJsonLayer(infoUpdate);

layerControl.addOverlay(geoJsonLayer, 'trajectory');

geoJsonLayer.addTo(map);

// 获取 CSV 文件并解析为数组
fetch('../data/8.1-7.geojson')
    .then(response => response.json())
    .then(data => {
        // geoJsonLayer.updateData(toGeoJson(hull));
        geoJsonLayer.updateData(data, (d) => parseInt(d.properties.COUNT_));
    })
    .catch(error => {
        console.error('获取或解析 CSV 文件出错:', error);
});
