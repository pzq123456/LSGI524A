import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm
import os


# 加载数据 CSV
# DS = pd.read_csv('src/simple/track/DS20.csv')['DS']

# 封装
def dsbar(DSpathArr, YEARArr):
    colors = ['#41b6c4','#fcc5c0']
    DS = []
    for DSpath in DSpathArr:
        # 只保留小于 7000 m 的数据
        tmp = pd.read_csv(DSpath)['DS']
        tmp = tmp[tmp < 7000]
        DS.append(tmp)

    for i in range(len(DS)):
        plt.hist(DS[i], bins=100, alpha=0.5, label=YEARArr[i], density=True, edgecolor='black', color=colors[i])


        
    # 拟合分布曲线 使用 scipy.stats.norm.fit() 拟合正态分布
    for i in range(len(DS)):
        mu, sigma = norm.fit(DS[i])
        x = np.linspace(DS[i].min(), DS[i].max(), 1000)
        y = norm.pdf(x, mu, sigma)
        plt.plot(x, y, label='N(' + str(round(mu, 2)) + ',' + str(round(sigma, 2)) + ')' + ' ' + YEARArr[i], color=colors[i])
    # x 轴 刻度增加
    plt.xticks(np.arange(0, 7000, 200))

    # 添加标题
    plt.title('Riding Distance Distribution of ' + YEARArr[0] + ' and ' + YEARArr[1], fontsize=20)
    # 添加标签
    plt.xlabel('Riding Distance (m)', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)

    plt.legend()
    # 显示
    plt.show()

# 封装
def dubar(DupathArr, YEARArr):
    colors = ['#41b6c4','#fcc5c0']

    DU = []
    for Dupath in DupathArr:
        tmp = pd.read_csv(Dupath)['DU']
        tmp = tmp[tmp < 120] 
        DU.append(tmp)

    for i in range(len(DU)):
        plt.hist(DU[i], bins=120, alpha=0.5, label=YEARArr[i], density=True, edgecolor='black', color=colors[i])


        
    # 拟合分布曲线 使用 scipy.stats.norm.fit() 拟合正态分布
    for i in range(len(DU)):
        mu, sigma = norm.fit(DU[i])
        x = np.linspace(DU[i].min(), DU[i].max(), 1000)
        y = norm.pdf(x, mu, sigma)
        plt.plot(x, y, label='N(' + str(round(mu, 2)) + ',' + str(round(sigma, 2)) + ')' + ' ' + YEARArr[i], color=colors[i])

    plt.xticks(np.arange(0, 120, 5))

    # 添加标题
    plt.title('Riding Duration Distribution of ' + YEARArr[0] + ' and ' + YEARArr[1], fontsize=20)
    # 添加标签
    plt.xlabel('Riding Duration (min)', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)

    plt.legend()
    # 显示
    plt.show()

if __name__ == '__main__':

    DIR = os.path.dirname(__file__)

    Paths1 = [os.path.join(DIR, 'simple', 'track', 'DS16.csv'), os.path.join(DIR, 'simple', 'track', 'DS20.csv')]
    Years = ['2016', '2020']
    Paths2 = [os.path.join(DIR, 'simple', 'DU', 'DU16.csv'), os.path.join(DIR, 'simple', 'DU', 'DU20.csv')]

    dsbar(Paths1, Years)
    dubar(Paths2, Years)