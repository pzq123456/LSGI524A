import pandas as pd
import matplotlib.pyplot as plt

PARENT_PATH = 'assiment1/' # linux path

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

    



if __name__ == "__main__":
    # getDepartureTrips()
    getStationTrips()