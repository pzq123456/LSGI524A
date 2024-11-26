from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.collections import PolyCollection
# 3D axes
from mpl_toolkits.mplot3d import Axes3D

import os 


def hex_to_rgba(hex_color):
    """Convert hex color to RGBA."""
    hex_color = hex_color.lstrip('#')
    return [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)] + [1.0]

def hex_colormap_to_array(hex_colors):
    """Convert a list of hex colors to a NumPy array of RGBA values."""
    rgba_colors = [hex_to_rgba(color) for color in hex_colors]
    return np.array(rgba_colors)

# 生成每一个面的顶点

def polygon_under_graph(x, y):
    """
    Construct the vertex list which defines the polygon filling the space under
    the (x, y) line graph. This assumes x is in ascending order.
    """
    return [(x[0], 0.), *zip(x, y), (x[-1], 0.)]

def draw_3DPlot(PATH, YEAR):
    weekDayName = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
            10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
            20, 21, 22, 23]
    frequency = [] # 7 * 24

    # 首先读取数据
    data = pd.read_csv(PATH)


    data['ST'] = pd.to_datetime(data['ST'])
    # 添加星期几
    data['weekday'] = data['ST'].dt.weekday
    # 添加小时
    data['hour'] = data['ST'].dt.hour

    # 首先按照 weekday 分组，对于每一个 weekday 再按照 hour 分组统计数量
    grouped = data.groupby(['weekday', 'hour']).size().reset_index(name='count')

    # 生成 7 * 24 的矩阵
    for i in range(7):
        frequency.append([0] * 24)

    for index, row in grouped.iterrows():
        frequency[row['weekday']][row['hour']] = row['count']

    # 使用 numpy 对数据进行归一化
    frequency = np.array(frequency)
    # 计算每一个小时 占当天总数的比例
    frequency = frequency / frequency.sum(axis=1)[:, None]

    ax = plt.figure().add_subplot(projection='3d')

    verts = []
    for i in range(7):
        verts.append(polygon_under_graph(hours, frequency[i]))

    # 颜色倒序
    # facecolors = plt.cm.viridis(np.linspace(1, 0, 7))
    # print(facecolors)
    facecolors = ['#ffffd9','#edf8b1','#c7e9b4','#7fcdbb','#41b6c4','#1d91c0','#225ea8']
    facecolors = hex_colormap_to_array(facecolors)
    print(facecolors)


    poly = PolyCollection(verts, facecolors=facecolors, alpha=.7)
    ax.add_collection3d(poly, zs=range(7), zdir='y')
    # 加入 描边
    poly.set_edgecolor('k')
    # 绘制 数据点
    for i in range(7):
        ax.scatter(hours, [i] * 24, frequency[i], c='k', s=3)


    ax.set(xlim=(0, 23),
            ylim=(0, 7), 
            zlim=(0, 0.2),
            xlabel='hour', 
            ylabel='weekday', 
            zlabel='frequency',
        )

    # X 轴更长
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1.5, 1.5, 1, 1.5]))

    # 减少 x 轴的标签并旋转
    ax.set_xticks(hours[::4])
    ax.set_xticklabels(hours[::4], rotation=0, fontsize=14) # 调整 xlabel 旋转
    # add weekday names
    ax.set_yticks(range(7))
    ax.set_yticklabels(weekDayName)

    # 图例
    # legend 每一个颜色对应一个 weekday
    legend = []
    for i in range(7):
        legend.append(plt.Line2D([0], [0], linestyle='none', c=facecolors[i], marker='o'))

    ax.legend(legend, weekDayName, loc='upper right')

    # add title
    plt.title(YEAR + ' Frequency of Riding by Weekday and Hour', fontsize=20)

    plt.show()

if __name__ == '__main__':
    DIR = os.path.dirname(__file__)
    # src/simple/cdf16.csv'
    PATH1 = os.path.join(DIR, 'simple', 'cdf16.csv')
    PATH2 = os.path.join(DIR, 'simple', 'cdf20.csv')

    draw_3DPlot(PATH1, '2016')
    draw_3DPlot(PATH2, '2020')