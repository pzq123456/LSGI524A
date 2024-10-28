import { initDom } from './utils.js';
import { baseMapInfos } from './baseMaps.js';
import { initCanvasLayer } from './canvaslayer.js';
import { getBaseMap } from './utils.js';

initDom(document.getElementById('map')); // set the map size to the screen size

let map = L.map('map',
    {
        renderer: L.canvas(),
    }
).setView([40.750997, -73.990619], 13);

let baseMaps = getBaseMap(baseMapInfos);
let layerControl = L.control.layers(baseMaps).addTo(map);
baseMaps["dark_all"].addTo(map);

initCanvasLayer();

function customPopupRenderer(info){
    let res =  `<div>
        <h3>Info</h3>
        <p>Intersection: ${info.intersection}</p>
        <p>Latitude: ${info.lat}</p>
        <p>Longitude: ${info.lon}</p>
        <p>Count: ${info.count}</p>
    </div>`;
    return res;
}

const mycolors = [ // 红色基调的暖色调
    '#f7f4f9', '#fde0dd', '#fcbba1',
    '#fc9272', '#fb6a4a', '#ef3b2c', '#99000d'
];

// let generatedColors = generateDistinctColors(123456, 41);

// generatedColors.push('gray');

const canvasLayer1 = L.canvasLayer(customPopupRenderer);
const canvasLayer2 = L.canvasLayer(customPopupRenderer);
const canvasLayer3 = L.canvasLayer(customPopupRenderer);

layerControl.addOverlay(canvasLayer1, 'departure');
layerControl.addOverlay(canvasLayer2, 'arrival');


canvasLayer2.setColors(mycolors);
canvasLayer2.addTo(map);

layerControl.expand();

// assiment2\data\intersections.csv
// 1,40.706991,-74.017946
// 2,40.706175,-74.01793
// assiment2\data\arrival_trip_count.csv
// drop_off_intersection,count
// 52.0,14535
// 112.0,34704
// assiment2\data\departure_trip_count.csv
// pick_up_intersection,count
// 52.0,5926
// 112.0,50640
// 154.0,670

const fetchCSV = (url) => fetch(url).then(response => response.text());

Promise.all([
    fetchCSV('../data/intersections.csv'),
    fetchCSV('../data/departure_trip_count.csv'),
    fetchCSV('../data/arrival_trip_count.csv')
])
.then(([intersectionsCSV, departureCSV, arrivalCSV]) => {
    const intersections = Papa.parse(intersectionsCSV, {
        header: false, // 无表头
        dynamicTyping: true,
        skipEmptyLines: true,
    }).data;

    // console.log(intersections);
    
    const departureTrips = Papa.parse(departureCSV, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true
    }).data;


    departureTrips.forEach((d) => {
        const intersection = intersections.find(i => i[0] === d.pick_up_intersection);
        if (intersection) {
            d.lat = intersection[1];
            d.lon = intersection[2];
            d.intersection = d.pick_up_intersection;
        }
    });

    const arrivalTrips = Papa.parse(arrivalCSV, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true
    }).data;

    arrivalTrips.forEach((d) => {
        const intersection = intersections.find(i => i[0] === d.drop_off_intersection);
        if (intersection) {
            d.lat = intersection[1];
            d.lon = intersection[2];
            d.intersection = d.drop_off_intersection;
        }
    });


    // 处理出发数据
    canvasLayer1.appendData(departureTrips, 
        (d) => [parseFloat(d.lat), parseFloat(d.lon)],
        (d) => parseInt(d.count));

    // 处理到达数据
    canvasLayer2.appendData(arrivalTrips, 
        (d) => [parseFloat(d.lat), parseFloat(d.lon)],
        (d) => parseInt(d.count));

})
.catch(error => {
    console.error('获取或解析 CSV 文件出错:', error);
});