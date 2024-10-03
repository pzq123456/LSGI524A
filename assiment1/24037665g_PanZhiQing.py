## 24037665g_PanZhiQing.py ##

import pandas as pd
import tqdm

import dask.dataframe as dd
from pyproj import Transformer
from dask.diagnostics import ProgressBar

import matplotlib.pyplot as plt

import scipy.stats as stats
import numpy as np

from sklearn.cluster import DBSCAN


transformer = Transformer.from_crs("EPSG:4326", "EPSG:26916", always_xy=True) # lon, lat -> x, y

# data path
PARENT_PATH = 'assiment1' # linux path
# PARENT_PATH = 'G:/polyulessons/LSGI524A/assiment1' # windows path

PATH1 = PARENT_PATH + '/data/chicago_data.csv'
PATH2 = PARENT_PATH + '/data/station.csv'

SAVE_PATH1 = PARENT_PATH + '/data/chicago_data_cleaned.csv'
SAVE_PATH2 = PARENT_PATH + '/data/station_cleaned.csv'
SAVE_PATH3 = PARENT_PATH + '/data/locations.csv' 

SAVE_PATH4 = PARENT_PATH + '/data/output.csv'

SAVE_PATH5 = PARENT_PATH + '/data/ststion_transformed.csv'
SAVE_PATH6 = PARENT_PATH + '/data/clustered_bike_stations_with_clusters.csv'
SAVE_PATH7 = PARENT_PATH + '/data/clustered_bike_stations.csv'


# ================== Task 1 ================== #


# clean the chicago data
def clean_chicago_data():
    df = pd.read_csv(PATH1)
    # 1. Drop  columns  that  will  not  be  used
    toDrop =  ['usertype','gender','birthyear']
    df = df.drop(toDrop, axis=1)
    # 2. Drop records whose start_time and end_time are not between 00:00:00 and 23:59:59, 25 July 2019
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    # pick up between 00:00:00 and 23:59:59 on 25 July 2019
    df = df[(df['start_time'] >= pd.to_datetime('2019-07-25 00:00:00')) & 
            (df['start_time'] <= pd.to_datetime('2019-07-25 23:59:59'))]

    df = df[(df['end_time'] >= pd.to_datetime('2019-07-25 00:00:00')) & 
            (df['end_time'] <= pd.to_datetime('2019-07-25 23:59:59'))]


    # 3. Drop records with any missing values
    df = df.dropna()
    # 指定 id 类型为 int
    df['trip_id'] = df['trip_id'].astype(int)
    df['bikeid'] = df['bikeid'].astype(int)
    df['from_station_id'] = df['from_station_id'].astype(int)
    df['to_station_id'] = df['to_station_id'].astype(int)
    # save the cleaned data 
    df.to_csv(SAVE_PATH1, index=False)

# clean the station data
def clean_station_data():
    df = pd.read_csv(PATH2)
    df = df[['data__stations__station_id', 'data__stations__name', 'data__stations__lat', 'data__stations__lon']]
    df.columns = ['id', 'name', 'lat', 'lon']
    df.to_csv(SAVE_PATH2, index=False)

# Drop records whose station ids are not in station.csv. 
def drop_invalid_station():
    df1 = pd.read_csv(SAVE_PATH1)
    df2 = pd.read_csv(SAVE_PATH2)
    valid_station_id = set(df2['id'])
    df1 = df1[(df1['from_station_id'].isin(valid_station_id)) & (df1['to_station_id'].isin(valid_station_id))]
    df1.to_csv(SAVE_PATH1, index=False)

# load the cleaned data and get the answer
def get_answer_task1():
    df = pd.read_csv(SAVE_PATH1)
    # 1) How many valid bicycle trips were documented on 25 July 2019? 
    print('1) How many valid bicycle trips were documented on 25 July 2019? ', len(df))
    # 2) How many bike stations were used on that day? (unique station both in from and to)
    print('2) How many bike stations were used on that day? ', len(set(df['from_station_id'].unique()) | set(df['to_station_id'].unique())))
    # 3) How many unique bikes were used?
    print('3) How many unique bikes were used? ', len(df['bikeid'].unique()))

# main function

def getLocations():
    print('get O-D locations(Lon,Lat) for each trip...')
    # chicago_data_cleaned 中记录的 from_station_id 和 to_station_id
    # 从 station_cleaned 中找到对应的经纬度 并按照顺序存储到 locations.csv
    # columns : trip_id, from_station_id, to_station_id, from_lat, from_lon, to_lat, to_lon
    df1 = pd.read_csv(SAVE_PATH1)
    df2 = pd.read_csv(SAVE_PATH2)
    df2 = df2.set_index('id')
    locations = []
    # for index, row in df1.iterrows():
    for index, row in tqdm.tqdm(df1.iterrows(), total=df1.shape[0]):
        from_id = row['from_station_id']
        to_id = row['to_station_id']
        from_lat = df2.loc[from_id]['lat']
        from_lon = df2.loc[from_id]['lon']
        to_lat = df2.loc[to_id]['lat']
        to_lon = df2.loc[to_id]['lon']
        locations.append([row['trip_id'], from_id, to_id, from_lat, from_lon, to_lat, to_lon])
    
    locations = pd.DataFrame(locations, columns=['trip_id', 'from_station_id', 'to_station_id', 'from_lat', 'from_lon', 'to_lat', 'to_lon'])
    # 指定 id 类型为 int
    locations['trip_id'] = locations['trip_id'].astype(int)
    locations['from_station_id'] = locations['from_station_id'].astype(int)
    locations['to_station_id'] = locations['to_station_id'].astype(int)
    locations.to_csv(SAVE_PATH3, index=False)
    print('locations saved to', SAVE_PATH3)

def task1():
    '''
    **Usage**:
        - run the ```task1()``` function or the following code in the terminal
        - ``` python clean.py ```
        - the cleaned data will be saved to the data folder, and the answer will be printed.
    **Note**:
    need the directory structure as follows:
            /assiment1
                /data
                    chicago_data.csv
                    station.csv
                /src
                    clean.py
    '''

    clean_chicago_data()
    clean_station_data()
    drop_invalid_station()
    print('cleaned data saved to', SAVE_PATH1, 'and', SAVE_PATH2)
    get_answer_task1()


# ================== Task 2 ================== #

# 定义一个用于在分块中处理坐标转换和距离计算的函数
def transform_and_calculate_distance(partition):
    # 转换起点和终点的坐标
    from_x, from_y = transformer.transform(partition['from_lon'].values, partition['from_lat'].values)
    to_x, to_y = transformer.transform(partition['to_lon'].values, partition['to_lat'].values)

    # 将转换后的坐标添加到数据分块中
    partition['from_x_transformed'] = from_x
    partition['from_y_transformed'] = from_y
    partition['to_x_transformed'] = to_x
    partition['to_y_transformed'] = to_y

    # 计算欧氏距离
    partition['distance'] = ((to_x - from_x) ** 2 + (to_y - from_y) ** 2) ** 0.5
    return partition



def getProjectedDistance(SAVE_PATH3, SAVE_PATH4):
    # 读取数据
    df = dd.read_csv(SAVE_PATH3)

    # 提供精确的 meta 信息，确保包含所有列及其类型
    meta = pd.DataFrame({
        'trip_id': pd.Series(dtype='int32'),
        'from_station_id': pd.Series(dtype='int32'),
        'to_station_id': pd.Series(dtype='int32'),
        'from_lat': pd.Series(dtype='float32'),
        'from_lon': pd.Series(dtype='float32'),
        'to_lat': pd.Series(dtype='float32'),
        'to_lon': pd.Series(dtype='float32'),
        'from_x_transformed': pd.Series(dtype='float32'),
        'from_y_transformed': pd.Series(dtype='float32'),
        'to_x_transformed': pd.Series(dtype='float32'),
        'to_y_transformed': pd.Series(dtype='float32'),
        'distance': pd.Series(dtype='float32')
    })

    # 使用 map_partitions 逐块转换坐标并计算距离
    df = df.map_partitions(transform_and_calculate_distance, meta=meta)

    # 显示进度条并保存结果
    with ProgressBar():
        df.to_csv(SAVE_PATH4, index=False, single_file=True)

# Trip duration : Max value, Min value, Median, Mean, 25% percentile, 75% percentile, Standard deviation
def getStatistics(column, title="Statistics"):
    # save the statistics as a dictionary
    statistics = {
        'Max value': column.max(),
        'Min value': column.min(),
        'Median': column.median(),
        'Mean': column.mean(),
        '25% percentile': column.quantile(0.25),
        '75% percentile': column.quantile(0.75),
        'Standard deviation': column.std()
    }

    print(title)
    # print the statistics
    for key, value in statistics.items():
        print(key, ': ', value)
    
    return statistics


def visualizeStatistics(statistics, title="Boxplot with Standard Deviation"):
    fig, ax = plt.subplots()
    
    box_data = [
        [statistics['Min value'], statistics['25% percentile'], statistics['Median'], statistics['75% percentile'], statistics['Max value']]
    ]
    positions = [1]
    widths = 0.5
    ax.boxplot(box_data, positions=positions, widths=widths)
    ax.set_title(title)
    plt.show()

def task2():
    # load the cleaned data
    df = pd.read_csv(SAVE_PATH1)
    # get the statistics of the trip duration
    trip_duration = df['tripduration']
    # convert the str to numeric as int ignore the numbers afther the dot
    trip_duration = pd.to_numeric(trip_duration, errors='coerce').dropna().astype(int)
    # get the statistics
    trip_duration_statistics = getStatistics(trip_duration, title="Trip Duration Statistics")
    # if you want to visualize the statistics
    # visualizeStatistics(trip_duration_statistics, title = "Trip Duration Boxplot with Standard Deviation")

    # load the cleaned data
    df = pd.read_csv(SAVE_PATH4)
    # get the statistics of the trip duration
    trip_distances = df['distance']
    # save 2 decimal points
    trip_distances = pd.to_numeric(trip_distances, errors='coerce').dropna().round(2)
    # 剔除异常值 0.0
    trip_distances = trip_distances[trip_distances != 0.0]
    # get the statistics
    trip_distances_statistics = getStatistics(trip_distances, title="Trip Distance Statistics")
    # if you want to visualize the statistics
    # visualizeStatistics(trip_distances_statistics, title = "Trip Distance Boxplot with Standard Deviation")

# ================== Task 3 ================== #
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

def task3():
    # Q1
    getDepartureTrips()
    # Q2
    getStationTrips()
    # Q3
    getTripDistanceDistribution()
    # Q4
    getTravelTimeDistribution()
    getTravelTimeDistribution2()
    getTravelTimeDistribution3()

# ================== Task 4 ================== #
def cluster_stations():
    # Step 1: Load the dataset using Dask
    print("Loading dataset...")
    with ProgressBar():
        data = dd.read_csv(SAVE_PATH5)
        stations = data[['id', 'x_transformed', 'y_transformed']].compute()
    
    # Step 2: Apply DBSCAN with a progress message
    print("Clustering stations...")
    db = DBSCAN(eps=600, min_samples=2)
    
    # Wrap DBSCAN with tqdm progress bar
    stations['cluster'] = tqdm(db.fit_predict(stations[['x_transformed', 'y_transformed']]), 
                               desc="Running DBSCAN")

    # Step 3: Merge cluster labels back to the original data
    print("Merging results...")
    with ProgressBar():
        data = data.merge(stations[['id', 'cluster']], on='id', how='left')

    # Step 4: Compute the final result with progress
    print("Computing final results...")
    with ProgressBar():
        result = data.compute()

    # Step 5: Filter clusters and group stations
    print("Filtering clusters...")
    clusters = result[result['cluster'] != -1]

    print("Grouping station IDs by clusters...")
    clustered_stations = clusters.groupby('cluster')['id'].apply(list).reset_index()

    # Step 6: Get number of clusters and output results
    num_clusters = clustered_stations.shape[0]
    print(f"Number of clusters: {num_clusters}")
    print("Station IDs in each cluster:")
    print(clustered_stations)

    # Step 7: Save the results to CSV files
    print("Saving results to CSV...")
    result.to_csv(SAVE_PATH6, index=False)
    clustered_stations.to_csv(SAVE_PATH7, index=False)

    print("Clustering completed.")

if __name__ == '__main__':
    # task 1
    task1()
    # attach the locations to the cleaned data not for the task1
    getLocations()

    # task 2
    getProjectedDistance(SAVE_PATH3, SAVE_PATH4) # get the projected distance
    task2()

    # task 3
    task3()

    # task 4
    cluster_stations()

