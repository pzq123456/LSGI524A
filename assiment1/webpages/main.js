import { initDom } from './utils.js';
import { baseMapInfos } from './baseMaps.js';
import { initCanvasLayer } from './canvaslayer.js';
import { getBaseMap } from './utils.js';

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
    return `<div>
        <h3>Info</h3>
        <p>Latitude: ${info.lat}</p>
        <p>Longitude: ${info.lon}</p>
        <p>Name: ${info.name}</p>
        <p>Departure: ${info.departure}</p>
        <p>Arrival: ${info.arrival}</p>
    </div>`;
}


// const mybreaks = [0, 1010, 2005, 3000, 3995, 4990, 5985, 6980, 7976, 8971, 9966, 10961, 11956, 12951, 13946, 14941, 15937]

// const mycolors = ['#f7fcf5', '#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#006d2c', '#00441b', '#003d19', '#003617', '#003015', '#002b13', '#002611', '#00200f', '#001b0d', '#00160b']
const mycolors = [ // 红色基调的暖色调
    '#f7f4f9', '#fde0dd', '#fcbba1',
    '#fc9272', '#fb6a4a', '#ef3b2c', '#99000d'
];

const canvasLayer1 = L.canvasLayer(customPopupRenderer);
const canvasLayer2 = L.canvasLayer(customPopupRenderer);

layerControl.addOverlay(canvasLayer1, 'departure');
layerControl.addOverlay(canvasLayer2, 'arrival');

canvasLayer2.setColors(mycolors);
canvasLayer2.addTo(map);

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
