// 获取屏幕宽高
function getScreenSize() {
    let width = window.innerWidth;
    let height = window.innerHeight;
    return { width, height };
}

// 设置某一个元素的宽高
function setElementSize(element, width, height) {
    element.style.width = width + 'px';
    element.style.height = height + 'px';
}

// 控制元素居中
function centerElement(element) {
    let { width, height } = getScreenSize();
    element.style.position = 'absolute';
    element.style.left = (width - element.offsetWidth) / 2 + 'px';
    element.style.top = (height - element.offsetHeight) / 2 + 'px';
}

export function initDom(element) {
    let { width, height } = getScreenSize();

    // 80%
    width = width * 0.95;
    height = height * 0.95;
    setElementSize(element, width, height);
    centerElement(element);
}

export function getBaseMap(baseMapInfos){
    let baseMaps = {};
    for(let item of baseMapInfos){
        baseMaps[item.name] = L.tileLayer(item.url+item.style+'/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: item.attribution
        });
    }
    return baseMaps;
}

function randomPoint(center, radius){
    let x0 = center[0];
    let y0 = center[1];
    let rd = Math.random() * radius;
    let theta = Math.random() * 2 * Math.PI;
    let x = x0 + rd * Math.cos(theta);
    let y = y0 + rd * Math.sin(theta);
    return [x, y];
}

function randomPointsWithProperties(center, radius, num){
    let points = [];
    for(let i=0; i<num; i++){
        let point = randomPoint(center, radius);
        
        point.push({
            "lat": point[0],
            "lng": point[1],
            "value": Math.random() * 100
        });

        points.push(point);
    }

    return points;
}

export function addColumn2GeoJson(geoJson, data, match_fn = eu_match, columnName = 'count') {
    let updatedGeoJson = JSON.parse(JSON.stringify(geoJson));
    updatedGeoJson.features.forEach((feature, index) => {
        const matchedValue = match_fn(feature.properties, data);
        feature.properties[columnName] = matchedValue;
    });
    return updatedGeoJson;
}

// 根据传入的属性值构造一个下拉框及一个按钮
export function createSelectAndButton(parent, options, buttonName, buttonClickHandler, style = {}, info = "info") {
    let infoElement = document.createElement('div');
    infoElement.innerText = info;
    parent.appendChild(infoElement);

    let select = document.createElement('select');
    for (let option of options) {
        let optionElement = document.createElement('option');
        optionElement.value = option;
        optionElement.innerText = option;
        select.appendChild(optionElement);
    }
    parent.appendChild(select);

    let button = document.createElement('button');
    button.innerText = buttonName;
    button.onclick = buttonClickHandler;
    parent.appendChild(button);

    // style for father element
    // for (let key in style) {
    //     parent.style[key] = style[key];
    // }

    // {
    //     'parent' : {
    //         'color': 'black',
    //     },
    //     'select': {
    //         'margin': '5px',
    //     },
    //     'button': {
    //         'margin': '5px',
    //     }
    // }

    // style for select element
    for (let key in style.select) {
        select.style[key] = style.select[key];
    }

    // style for button element
    for (let key in style.button) {
        button.style[key] = style.button[key];
    }

    // style for info element
    for (let key in style.parent) {
        parent.style[key] = style.parent[key];
    }

    // style for info element
    for (let key in style.info) {
        infoElement.style[key] = style.info[key];
    }

    return select;
}