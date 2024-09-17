import pandas as pd
import matplotlib.pyplot as plt

PARENT_PATH = 'LSGI524A/assiment1' # linux path

SAVE_PATH1 = PARENT_PATH + '/data/chicago_data_cleaned.csv'
SAVE_PATH2 = PARENT_PATH + '/data/station_cleaned.csv'
SAVE_PATH3 = PARENT_PATH + '/data/locations.csv' 

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

    # 统计每个站点的出发和到达行程数量
    departure_counts = data.groupby('from_station_name')['trip_id'].count()
    arrival_counts = data.groupby('to_station_name')['trip_id'].count()

    # 将出发和到达行程数量合并到同一个DataFrame中
    station_counts = pd.DataFrame({
        'Departures': departure_counts,
        'Arrivals': arrival_counts
    }).fillna(0)  # 如果某些站点没有出发或到达行程，用0填充

    # 绘制堆叠柱状图
    station_counts.plot(kind='bar', stacked=True, figsize=(10, 6), color=['skyblue', 'orange'])

    # 设置图表标题和标签
    plt.title('Distribution of Departure and Arrival Trips by Station')
    plt.xlabel('Station Name')
    plt.ylabel('Number of Trips')

    # 显示图表
    plt.xticks(rotation=90)  # X轴标签旋转90度以便清晰显示
    plt.tight_layout()  # 自动调整图表布局
    plt.show()


if __name__ == "__main__":
    # getDepartureTrips()
    getStationTrips()