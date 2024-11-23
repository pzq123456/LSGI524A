import { createSelectAndButton } from './utils.js';
import { baseMapInfos } from './baseMaps.js';
import { initCanvasLayer } from './canvaslayer.js';
import { getBaseMap } from './utils.js';
import { initGeoJsonLayer } from './geojsonlayer.js';
import { interpolateColors, interpolateColorsEx, getRandomLightColor, getRandomDarkColor } from './color.js';

// initDom(document.getElementById('map')); // set the map size to the screen size

// get btn1
const btn1 = document.getElementById('btn1');
// get .toolbar
const toolbar = document.querySelector('.toolbar');


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
    const contents = props ? `<b>RoadID : ${props.RoadID}</b><br/> Index : ${props.MEAN_Tree} ` : 'Hover over a trajectory';
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

// "RoadID": 1, "MEAN_Build": 0.0, "MEAN_Car": 0.0, "MEAN_Perso": 0.0, "MEAN_Rider": 0.0, "MEAN_Road": 0.0, "MEAN_RoadS": 0.0, "MEAN_Sky": 0.0, "MEAN_Tree": 0.0, "Shape_Leng": 6.7557670355399999 }

// const C_Colors = interpolateColors("red","white", 16);
const C_Colors = interpolateColorsEx("red", "green", "blue", 16);

btn1.onclick = function () {
    console.log(geoJsonLayer2.getColumns());
    geoJsonLayer.setColors(C_Colors);
    geoJsonLayer2.setColumn('MEAN_Tree');
};

const columns = ['MEAN_Car', 'MEAN_Perso', 'MEAN_Rider', 'MEAN_Road', 'MEAN_RoadS', 'MEAN_Sky', 'MEAN_Tree', 'Shape_Leng'];


// 为每一种颜色生成一种颜色
let colorset = {}
columns.forEach((column) => {
    colorset[column] = interpolateColors(getRandomLightColor(), getRandomDarkColor(), 16);
});

// create a select and a button
createSelectAndButton(toolbar, columns, 'Update', function () {
    const selectedColumn = document.querySelector('select').value;
    geoJsonLayer2.setColumn(selectedColumn, colorset[selectedColumn]);
});