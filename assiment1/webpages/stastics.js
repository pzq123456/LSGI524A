export class Stastics{ // 单值统计
    constructor(){
        this._max = 0;
        this._min = 0;
        this._average = 0;
        this._data = [];
    }

    clear(){
        this._max = 0;
        this._min = 0;
        this._average = 0;
        this._data = [];
    }

    update(){
        // console.log(this._data);
        this._max = Math.max(...this._data);
        this._min = Math.min(...this._data);
        this._average = this._data.reduce((a, b) => a + b, 0) / this._data.length;
    }

    append(value, getVal){
        // 将数据添加到数组中
        this._data.push(...value.map(getVal));
        this.update();
        console.log(this._max, this._min, this._average);
    }

    // 根据内置的统计值进行值映射
    mapValue(value, isReverse = false){
        if(isReverse){
            return 1 - (value - this._min) / (this._max - this._min);
        }else{
            return (value - this._min) / (this._max - this._min);
        }
    }

    /**
     * 支持简易的离散值映射
     */
    mapValue2Color(value, isReverse = false, colors = defaultColors){
        let index = Math.floor(this.mapValue(value, isReverse) * (colors.length - 1));
        return colors[index];
    }

    getGrades(num){ // 获取分级
        let grades = [];
        let step = (this._max - this._min) / num;
        for (let i = 0; i < num; i++){
            grades.push(this._min + i * step);
        }
        grades.push(this._max);
        return grades;
    }
}

// const defaultColors  = [
//     '#00441b', '#f7fbff', '#deebf7', '#9ecae1', 
//     '#6baed6', '#3182bd', '#08519c', '#08306b'
// ];

const defaultColors = [ // 红色基调的暖色调
    '#67000d', '#f7f4f9', '#fde0dd', '#fcbba1',
    '#fc9272', '#fb6a4a', '#ef3b2c', '#99000d'
];

//   #f7fbff
  
// const defaultColors = ['#f7fcf5', '#e5f5e0', '#c7e9c0', '#a1d99b', '#74c476', '#41ab5d', '#238b45', '#006d2c', '#00441b', '#003d19', '#003617', '#003015', '#002b13', '#002611', '#00200f', '#001b0d', '#00160b'];