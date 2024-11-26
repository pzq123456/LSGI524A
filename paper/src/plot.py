import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

def compute_cdf(data):
    # 忽略 NaN 值
    data = data.dropna()
    # 将数据排序
    sorted_data = np.sort(data)
    n = len(sorted_data)
    # 计算每个时间间隔的累积概率
    cdf = np.arange(1, n + 1) / n
    return sorted_data, cdf

def compute_pdf(data):
    data = data.dropna()

    # 将数据排序
    sorted_data = np.sort(data)
    n = len(sorted_data)
    # 计算每个时间间隔的概率密度
    pdf = np.ones(n) / n
    return sorted_data, pdf

# 封装为函数
def cdf(path):
    '''
    数据格式：
    UID,ST
    1,2020-01-01 00:00:00
    1,2020-01-01 01:00:00
    2,2020-01-01 00:00:00
    ...
    函数效果：
    读取数据文件，计算每个 UID 的时间间隔，绘制时间间隔的 CDF 图
    '''
    # 读取数据
    df = pd.read_csv(path)
    df['ST'] = pd.to_datetime(df['ST'])
    df = df.sort_values(by=['UID', 'ST'])
    df['TimeDiff'] = df.groupby('UID')['ST'].diff().dt.total_seconds() / 3600

    # 使用 compute_cdf 函数计算 CDF
    sorted_data, cdf = compute_cdf(df['TimeDiff'])
    return sorted_data,cdf

    # # 绘制 CDF 图
    # plt.plot(sorted_data, cdf)
    # plt.xlabel('Time Interval (hours)')
    # plt.ylabel('CDF')
    # plt.title('CDF of Time Interval')
    # plt.grid(True)
    # plt.show()

def plot_cdf(cdfs,names,styles):
    '''
    函数效果：
    绘制多个 CDF 图
    '''
    for i in range(len(cdfs)):
        plt.plot(cdfs[i][0], cdfs[i][1], label=names[i], linestyle=styles[i])
    plt.xlabel('Time Interval (hours)', fontsize=20)
    plt.ylabel('CDF', fontsize=20)
    plt.title('CDF of Time Interval', fontsize=20)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True)
    plt.legend()
    plt.show()


def plot_pdf(path):
    '''
    数据格式：
    UID,ST
    1,2020-01-01 00:00:00
    1,2020-01-01 01:00:00
    2,2020-01-01 00:00:00
    ...
    函数效果：
    读取数据文件，计算每个 UID 的时间间隔，绘制时间间隔的 PDF 曲线
    '''
    # 读取数据
    df = pd.read_csv(path)
    df['ST'] = pd.to_datetime(df['ST'])  # 将时间列转换为日期时间类型
    df = df.sort_values(by=['UID', 'ST'])  # 按照 UID 和时间排序
    df['TimeDiff'] = df.groupby('UID')['ST'].diff().dt.total_seconds() / 3600  # 计算时间间隔（小时）

    df = df.dropna(subset=['TimeDiff'])  # 删除时间差为空的行

    # 使用 seaborn 绘制核密度估计（KDE）曲线
    kde = sns.kdeplot(df['TimeDiff'], fill=True, color='g', label='PDF of Time Interval')

    # 设置标题和标签
    plt.xlabel('Time Interval (hours)', fontsize=14)
    plt.ylabel('PDF', fontsize=14)
    plt.title('PDF of Time Interval', fontsize=20)

    # 添加图例
    plt.legend(fontsize=14)

    # 设置网格
    plt.grid(True)

    # 显示图形
    plt.show()




if __name__ == '__main__':

    DIR = os.path.dirname(__file__)
    PATH1 = os.path.join(DIR, 'simple', 'cdfs16.npy')
    PATH2 = os.path.join(DIR, 'simple', 'cdf16.csv')

    # plot_cdf('src\simple\cdf20.csv')
    # 绘制 2016 年和 2020 年的 CDF 图
    cdfs = []
    cdfs.append(np.load(PATH1, allow_pickle=True))
    names = ['2016']
    styles = ['-']

    # cdfs.append(cdf('/simple/cdf16.csv'))
    # cdfs.append(cdf('/simple/cdf20.csv'))
    # # 保存 cdfs 文件为 npy 文件
    # np.save('cdfs16.npy', cdfs[0])
    # np.save('cdfs20.npy', cdfs[1])

    # plot_cdf(cdfs, names, styles)

    plot_pdf(PATH2)

    # # 加载 cdfs.npy 文件
    # # cdfs = np.load('src/simple/cdfs.npy', allow_pickle=True)
    # # 只绘制 2016 年的 CDF 图
    # plot_cdf([cdfs[0]], [names[0]], [styles[0]]) 