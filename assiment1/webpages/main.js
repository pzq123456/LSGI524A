import { initDom } from './utils.js';
import { baseMapInfos } from './baseMaps.js';
import { initCanvasLayer } from './canvaslayer.js';
import { getBaseMap } from './utils.js';

import * as RVGeo from './rvgeo.js';

console.log(RVGeo);

initDom(document.getElementById('map')); // set the map size to the screen size

let map = L.map('map',
    {
        renderer: L.canvas(),
    }
).setView([41.878287, -87.643909], 13);

let baseMaps = getBaseMap(baseMapInfos);
let layerControl = L.control.layers(baseMaps).addTo(map);
baseMaps["dark_all"].addTo(map);

initCanvasLayer();

function customPopupRenderer(info){
    let res =  `<div>
        <h3>Info</h3>
        <p>Latitude: ${info.lat}</p>
        <p>Longitude: ${info.lon}</p>
        <p>Name: ${info.name}</p>
        <p>Departure: ${info.departure}</p>
        <p>Arrival: ${info.arrival}</p>
    </div>`;
    // x_transformed,y_transformed,cluster
    if(info.x_transformed !== undefined){
        res += `<h3>Cluster</h3>
        <p>x_transformed: ${info.x_transformed}</p>
        <p>y_transformed: ${info.y_transformed}</p>
        <p>cluster: ${info.cluster}</p>`;
    }
    return res;
}

const mycolors = [ // 红色基调的暖色调
    '#f7f4f9', '#fde0dd', '#fcbba1',
    '#fc9272', '#fb6a4a', '#ef3b2c', '#99000d'
];

let generatedColors = generateDistinctColors(123456, 41);

generatedColors.push('gray');

const canvasLayer1 = L.canvasLayer(customPopupRenderer);
const canvasLayer2 = L.canvasLayer(customPopupRenderer);
const canvasLayer3 = L.canvasLayer(customPopupRenderer);

layerControl.addOverlay(canvasLayer1, 'departure');
layerControl.addOverlay(canvasLayer2, 'arrival');
layerControl.addOverlay(canvasLayer3, 'cluster');


canvasLayer2.setColors(mycolors);
canvasLayer2.addTo(map);

canvasLayer3.setColors(generatedColors);

layerControl.expand();

// 获取 CSV 文件并解析为数组
fetch('../data/station_cleaned.csv')
    .then(response => response.text())
    .then(csvData => {
        // console.log(csvData);
        Papa.parse(csvData, {
            header: true, // 如果 CSV 有表头，设置为 true
            dynamicTyping: true, // 自动将数字和布尔值转换为对应类型
            skipEmptyLines: true, // 跳过空行
            worker: true, // 使用 Web Worker 处理 CSV

            chunk: function(results, parser) {
                // 同时向两个图层添加数据
                canvasLayer1.appendData(results.data, 
                    (d) => [parseFloat(d.lat), parseFloat(d.lon)],
                    (d) => parseInt(d.departure));
            },
        });
    })
    .catch(error => {
        console.error('获取或解析 CSV 文件出错:', error);
});

fetch('../data/station_cleaned.csv')
    .then(response => response.text())
    .then(csvData => {
        // console.log(csvData);
        Papa.parse(csvData, {
            header: true, // 如果 CSV 有表头，设置为 true
            dynamicTyping: true, // 自动将数字和布尔值转换为对应类型
            skipEmptyLines: true, // 跳过空行
            worker: true, // 使用 Web Worker 处理 CSV

            chunk: function(results, parser) {
                // 同时向两个图层添加数据
                canvasLayer2.appendData(results.data, 
                    (d) => [parseFloat(d.lat), parseFloat(d.lon)],
                    (d) => parseInt(d.arrival));
            },
        });
    })
    .catch(error => {
        console.error('获取或解析 CSV 文件出错:', error);
});

// 获取 CSV 文件并解析为数组
fetch('../data/clustered_bike_stations_with_clusters.csv')
    .then(response => response.text())
    .then(csvData => {
        // console.log(csvData);
        Papa.parse(csvData, {
            header: true, // 如果 CSV 有表头，设置为 true
            dynamicTyping: true, // 自动将数字和布尔值转换为对应类型
            skipEmptyLines: true, // 跳过空行
            worker: true, // 使用 Web Worker 处理 CSV

            chunk: function(results, parser) {
                // 同时向两个图层添加数据
                canvasLayer3.appendData(results.data, 
                    (d) => [parseFloat(d.lat), parseFloat(d.lon)],
                    (d) => parseInt(d.cluster));
            },
        });
    })
    .catch(error => {
        console.error('获取或解析 CSV 文件出错:', error);
});

// Function to convert HSL to RGB
function hslToRgb(h, s, l) {
    let c = (1 - Math.abs(2 * l - 1)) * s;
    let x = c * (1 - Math.abs((h / 60) % 2 - 1));
    let m = l - c / 2;
    let r = 0, g = 0, b = 0;
    
    if (0 <= h && h < 60) { r = c; g = x; b = 0; }
    else if (60 <= h && h < 120) { r = x; g = c; b = 0; }
    else if (120 <= h && h < 180) { r = 0; g = c; b = x; }
    else if (180 <= h && h < 240) { r = 0; g = x; b = c; }
    else if (240 <= h && h < 300) { r = x; g = 0; b = c; }
    else if (300 <= h && h < 360) { r = c; g = 0; b = x; }
    
    r = Math.round((r + m) * 255);
    g = Math.round((g + m) * 255);
    b = Math.round((b + m) * 255);
    
    return `rgb(${r}, ${g}, ${b})`;
}

// Seeded random number generator
function seededRandom(seed) {
    var m = 0x80000000; // 2^31
    var a = 1103515245;
    var c = 12345;

    seed = (a * seed + c) % m;
    return seed / m;
}

// Generate colors based on HSL model with large hue differences
function generateDistinctColors(seed, count) {
    let colors = [];
    let hueStep = 360 / count;  // Ensure large differences between adjacent hues

    for (let i = 0; i < count; i++) {
        seed = (seed * 9301 + 49297) % 233280; // Update seed for random variation
        
        let hue = (seededRandom(seed) * 360 + i * hueStep) % 360; // Spread hue across 360 degrees
        let saturation = 0.7;  // Fixed saturation for vibrant colors
        let lightness = 0.5;   // Fixed lightness for balanced brightness
        
        colors.push(hslToRgb(hue, saturation, lightness));
    }

    return colors;
}
