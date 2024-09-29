import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

PARENT_PATH = 'assiment1/' # linux path
# PARENT_PATH = 'G:/polyulessons/LSGI524A/assiment1' # windows path

SAVE_PATH1 = PARENT_PATH + '/data/chicago_data_cleaned.csv'
SAVE_PATH2 = PARENT_PATH + '/data/station_cleaned.csv'
SAVE_PATH3 = PARENT_PATH + '/data/locations.csv' 
SAVE_PATH4 = PARENT_PATH + '/data/output.csv'

#Q1: How does the number of departure trips change over 24 hours? Is there any rhythm or pattern?
def getDepartureTrips():
    df = pd.read_csv(SAVE_PATH1)
    # get the hour of the start time
    df['hour'] = pd.to_datetime(df['start_time']).dt.hour
    # group by the hour
    df = df.groupby('hour').size()
    # plot the number of departure trips
    df.plot(kind='bar', title='Number of Departure Trips over 24 hours')
    plt.xlabel('Hour')
    plt.ylabel('Number of Departure Trips')
    plt.show()

# Q2: What is the distribution of the number of departure trips at different stations? What about the distribution of arrival trips?
def getStationTrips():
    # 读取CSV文件
    data = pd.read_csv(SAVE_PATH1)
    # 读取station_cleaned.csv文件
    station = pd.read_csv(SAVE_PATH2)
    # station_cleaned.csv文件中的station_id和data.csv文件中的from_station_id和to_station_id相同
    # 统计出发及到达站点的次数 追加到station_cleaned.csv文件中
    station['departure'] = data.groupby('from_station_id').size()
    station['arrival'] = data.groupby('to_station_id').size()
    # 对于没有出发或到达的站点，将其次数设置为0
    station['departure'].fillna(0, inplace=True)
    station['arrival'].fillna(0, inplace=True)
    # 保存到CSV文件 还是保存到station_cleaned.csv文件中
    station.to_csv(SAVE_PATH2, index=False)

# (3) What is the distribution of the trip distance
#  (measured as straight-line Euclidean distance)? What will you conclude from this distribution? 
def getTripDistanceDistribution():
    # 读取CSV文件
    data = pd.read_csv(SAVE_PATH4)
    # 拟合分布曲线 正态分布 使用 scipy.stats.norm.fit() 拟合正态分布
    mu, sigma = stats.norm.fit(data['distance'])
    x = np.linspace(data['distance'].min(), data['distance'].max(), 1000)
    y = stats.norm.pdf(x, mu, sigma)
    # 绘制直方图
    plt.hist(data['distance'], bins=100, alpha=0.5, density=True, edgecolor='black')
    # 绘制拟合曲线
    plt.plot(x, y, label='N(mu=' + str(round(mu, 2)) + ',sigma=' + str(round(sigma, 2)) + ')')
    # 添加标题
    plt.title('Trip Distance Distribution')
    # 将拟合曲线的参数添加到图例中
    # 添加标签
    plt.xlabel('Distance (m)')
    plt.ylabel('Frequency')
    plt.legend()
    # 显示
    plt.show()

# (4) What is the distribution of the travel time (i.e., trip duration)?
def getTravelTimeDistribution():
    # 读取CSV文件
    data = pd.read_csv(SAVE_PATH1) # tripduration 为秒
    # tripduration
    # 拟合分布曲线 正态分布 使用 scipy.stats.norm.fit() 拟合正态分布
    mu, sigma = stats.norm.fit(data['tripduration'])
    x = np.linspace(data['tripduration'].min(), data['tripduration'].max(), 1000)
    y = stats.norm.pdf(x, mu, sigma)
    # 绘制直方图
    plt.hist(data['tripduration'], bins=100, alpha=0.5, density=True, edgecolor='black')
    # 绘制拟合曲线
    plt.plot(x, y, label='N(mu=' + str(round(mu, 2)) + ',sigma=' + str(round(sigma, 2)) + ')')
    # 添加标题
    plt.title('Travel Time Distribution')
    # 将拟合曲线的参数添加到图例中
    # 添加标签
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency')
    plt.legend()
    # 显示
    plt.show()

# (4) What is the distribution of the travel time (i.e., trip duration)? for start_time,end_time
# use different clolor to show the distribution of the travel time start_time,end_time
def getTravelTimeDistribution2():
    # 读取CSV文件
    data = pd.read_csv(SAVE_PATH1) # get start_time,end_time
    # no need to get tripduration
    str_time = pd.to_datetime(data['start_time']).dt.hour
    end_time = pd.to_datetime(data['end_time']).dt.hour

    # hist the two time
    plt.hist(str_time, bins=24, alpha=0.5, density=True, edgecolor='black',label='start_time')
    plt.hist(end_time, bins=24, alpha=0.5, density=True, edgecolor='black',label='end_time')
    # 添加标题
    plt.title('Travel Time Distribution')
    # 添加标签
    plt.xlabel('Time (h)')
    plt.ylabel('Frequency')
    plt.legend()
    # 显示
    plt.show()

def getTravelTimeDistribution3():
    # 读取CSV文件
    data = pd.read_csv(SAVE_PATH1) # get start_time,end_time
    # no need to get tripduration
    str_time = pd.to_datetime(data['start_time']).dt.hour
    end_time = pd.to_datetime(data['end_time']).dt.hour

    # heatmap the two time
    plt.hist2d(str_time,end_time,bins=24)
    # 添加标题
    plt.title('Heatmap of Travel Time Distribution')
    # 添加标签
    plt.xlabel('Start Time (h)')
    plt.ylabel('End Time (h)')
    # legend
    plt.colorbar()
    # 显示
    plt.show()













if __name__ == "__main__":
    # Q1
    # getDepartureTrips()
    # Q2
    # getStationTrips()
    # Q3
    # getTripDistanceDistribution()
    # Q4
    # getTravelTimeDistribution()
    # getTravelTimeDistribution2()
    getTravelTimeDistribution3()