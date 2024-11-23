import { createSelectAndButton } from './utils.js';
import { baseMapInfos } from './baseMaps.js';
import { initCanvasLayer } from './canvaslayer.js';
import { getBaseMap } from './utils.js';
import { initGeoJsonLayer } from './geojsonlayer.js';
import { interpolateColors, interpolateColorsEx, getRandomLightColor, getRandomDarkColor } from './color.js';

// initDom(document.getElementById('map')); // set the map size to the screen size

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
        geoJsonLayer.setColors(colorsets[1]);
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


const columns = ['MEAN_Car', 'MEAN_Road', 'MEAN_RoadS', 'MEAN_Sky', 'MEAN_Tree', 'Shape_Leng'];

const colorsets = [
    ['#f7fbff','#deebf7','#c6dbef','#9ecae1','#6baed6','#4292c6','#2171b5','#08519c','#08306b'], // blue
    ['#ffffd9','#edf8b1','#c7e9b4','#7fcdbb','#41b6c4','#1d91c0','#225ea8','#253494','#081d58'], // blue-green
    ['#ffffe5','#f7fcb9','#d9f0a3','#addd8e','#78c679','#41ab5d','#238443','#006837','#004529'], // green
    ['#f7f4f9','#e7e1ef','#d4b9da','#c994c7','#df65b0','#e7298a','#ce1256','#980043','#67001f'], // red
    ['#fcfbfd','#efedf5','#dadaeb','#bcbddc','#9e9ac8','#807dba','#6a51a3','#54278f','#3f007d'], // purple
    ['#fff5eb','#fee6ce','#fdd0a2','#fdae6b','#fd8d3c','#f16913','#d94801','#a63603','#7f2704'], // orange
    ['#fff7f3','#fde0dd','#fcc5c0','#fa9fb5','#f768a1','#dd3497','#ae017e','#7a0177','#49006a'], // pink
];

// create a select and a button
createSelectAndButton(toolbar, columns, 'Show', function () {
    const selectedColumn = document.querySelector('select').value;
    // 获取选择的 column 的 index
    const index = columns.indexOf(selectedColumn);
    // index 限制在颜色集的长度内 取余
    const colorset = colorsets[index % colorsets.length];
    // 设置颜色
    geoJsonLayer2.setColumn(selectedColumn, colorset);
}, {
    'parent' : {
        'color': 'black',
        'padding': '5px',
        'borderRadius': '5px',
        'margin': '5px',
        'border': '1px solid black',
        'backgroundColor': '#d9f0a3',
    },
    'select': {
        'margin': '5px',
        'borderRadius': '5px',
        'backgroundColor': '#f7fbff',
    },
    'button': {
        'margin': '5px',
        'width': '100px',
        'height': '40px',
        'borderRadius': '5px',
        'backgroundColor': '#4CAF50',
        'color': 'white',
    },
    'info': {
        'margin': '5px',
        'fontSize': '20px',
        'bold': 'true',
        'color': 'black',
    }
}

,"Select a column to show (colorSets form https://colorbrewer2.org/).");
