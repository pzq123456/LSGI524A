// 颜色名到RGB的映射
const colorNames = {
    "black": "#000000",
    "white": "#ffffff",
    "red": "#ff0000",
    "green": "#00ff00",
    "blue": "#0000ff",
    "yellow": "#ffff00",
    // 可以扩展更多颜色名
};

// 将颜色名转换为RGB
function nameToRGB(name) {
    if (colorNames[name.toLowerCase()]) {
        return hexToRGB(colorNames[name.toLowerCase()]);
    }
    throw new Error(`未知的颜色名: ${name}`);
}

// 将HEX转换为RGB
function hexToRGB(hex) {
    let r = parseInt(hex.slice(1, 3), 16);
    let g = parseInt(hex.slice(3, 5), 16); // 修正错误
    let b = parseInt(hex.slice(5, 7), 16);
    return { r, g, b, a: 1 };
}

// 将RGBA字符串转换为RGB
function rgbaToRGB(rgba) {
    let parts = rgba.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d?\.?\d+))?\)/);
    return { r: parseInt(parts[1]), g: parseInt(parts[2]), b: parseInt(parts[3]), a: parts[4] ? parseFloat(parts[4]) : 1 };
}

// 将HLS字符串转换为RGB（HLS转RGB的实现可在需要时补充）

// 解析输入颜色
function parseColor(color) {
    if (color.startsWith("#")) {
        return hexToRGB(color);
    } else if (color.startsWith("rgba") || color.startsWith("rgb")) {
        return rgbaToRGB(color);
    } else if (colorNames[color.toLowerCase()]) {
        return nameToRGB(color);
    } else {
        throw new Error(`无法解析颜色: ${color}`);
    }
}

// 颜色插值算法
export function interpolateColors(startColor, endColor, steps) {
    startColor = parseColor(startColor);
    endColor = parseColor(endColor);
    
    if (steps < 3) {
        throw new Error("分级个数不少于3");
    }

    const colors = [];
    for (let i = 0; i < steps; i++) {
        const t = i / (steps - 1);
        const r = Math.round(startColor.r + t * (endColor.r - startColor.r));
        const g = Math.round(startColor.g + t * (endColor.g - startColor.g));
        const b = Math.round(startColor.b + t * (endColor.b - startColor.b));
        colors.push(`rgb(${r}, ${g}, ${b})`);
    }

    return colors;
}

// 拓展的颜色插值算法 可以支持三种颜色的插值及透明度的插值
export function interpolateColorsEx(startColor, middleColor, endColor, steps) {
    startColor = parseColor(startColor);
    middleColor = parseColor(middleColor);
    endColor = parseColor(endColor);
    
    if (steps < 3) {
        throw new Error("分级个数不少于3");
    }

    const colors = [];
    for (let i = 0; i < steps; i++) {
        const t = i / (steps - 1);
        let r, g, b;
        if (t < 0.5) {
            r = Math.round(startColor.r + 2 * t * (middleColor.r - startColor.r));
            g = Math.round(startColor.g + 2 * t * (middleColor.g - startColor.g));
            b = Math.round(startColor.b + 2 * t * (middleColor.b - startColor.b));
        } else {
            r = Math.round(middleColor.r + 2 * (t - 0.5) * (endColor.r - middleColor.r));
            g = Math.round(middleColor.g + 2 * (t - 0.5) * (endColor.g - middleColor.g));
            b = Math.round(middleColor.b + 2 * (t - 0.5) * (endColor.b - middleColor.b));
        }
        colors.push(`rgb(${r}, ${g}, ${b})`);
    }

    return colors;
}


// 获取随机浅色
export function getRandomLightColor() {
    // 整数 0-255
    const r = Math.floor(Math.random() * 100 + 155);
    const g = Math.floor(Math.random() * 100 + 155);
    const b = Math.floor(Math.random() * 100 + 155);

    return `rgb(${r}, ${g}, ${b})`;

}

// 获取随机深色
export function getRandomDarkColor() {

    const r = Math.floor(Math.random() * 100);
    const g = Math.floor(Math.random() * 100);
    const b = Math.floor(Math.random() * 100);

    return `rgb(${r}, ${g}, ${b})`;
}

// 获取随机颜色
export function getRandomColor() {

    const r = Math.floor(Math.random() * 255);
    const g = Math.floor(Math.random() * 255);
    const b = Math.floor(Math.random() * 255);

    return `rgb(${r}, ${g}, ${b})`;
}
