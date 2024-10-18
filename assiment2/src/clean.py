import os
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ./data/
PARENT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data') # path to data directory
PATH1 = os.path.join(PARENT_PATH, 'taxi_id.csv.bz2') # path to the zipped file
PATH2 = os.path.join(PARENT_PATH, 'intersections.csv') # path to the zipped file

SAVE_PATH1 = os.path.join(PARENT_PATH, 'taxi_id.csv') # path to the unzipped file
SAVE_PATH2 = os.path.join(PARENT_PATH, 'taxi_id_clean.csv') # path to the cleaned file
SAVE_PATH3 = os.path.join(PARENT_PATH, 'trip_count_per_taxi.csv') # path to the trip count per taxi file
SAVE_PATH4 = os.path.join(PARENT_PATH, 'daily_trip_count.csv') # path to the daily trip count file

SAVE_PATH5 = os.path.join(PARENT_PATH, 'departure_trip_count.csv') # path to the departure trip count file
SAVE_PATH6 = os.path.join(PARENT_PATH, 'arrival_trip_count.csv') # path to the arrival trip count file

# 指定列名
taxi_columns = ['taxi_id', 'pick_up_time', 'drop_off_time', 'pick_up_intersection', 'drop_off_intersection']
inter_columns = ['id', 'latitude', 'longitude']

taxi_dtypes = {
    'taxi_id': 'float64',
    'pick_up_time': 'float64',  # 原始的 Unix 时间戳
    'drop_off_time': 'float64',  # 原始的 Unix 时间戳
    'pick_up_intersection': 'float64',
    'drop_off_intersection': 'float64'
}

# Q1 : How many unique taxis are there in this dataset, and how many trips are recorded?
def q1(stage_name):
    # stage_name = 'before' or 'after'
    with ProgressBar():
        if stage_name == 'before':
            print("Before cleaning:")
            print(f'Number of unique taxis: {taxi_df["taxi_id"].nunique().compute()}')
            print(f'Number of trips recorded: {taxi_df["taxi_id"].count().compute()}')
        elif stage_name == 'after':
            print("After cleaning:")
            print(f'Number of unique taxis: {cleaned_taxi_df["taxi_id"].nunique().compute()}')
            print(f'Number of trips recorded: {cleaned_taxi_df["taxi_id"].count().compute()}')

def clean(taxi_df, inter_df, SAVE_PATH2):
    valid_intersections = set(inter_df['id'])

    taxi_df = taxi_df.dropna()
    taxi_df = taxi_df.drop_duplicates()

    # 规则1：检查时间格式是否为有效的 Unix 时间
    current_timestamp = pd.Timestamp.now().timestamp()  # 获取当前 Unix 时间戳
    # 获取 2010 年 12 月 31 日的 Unix 时间戳
    start_timestamp = pd.Timestamp(year=2010, month=12, day=31).timestamp()
    taxi_df = taxi_df[
        (taxi_df['pick_up_time'] > start_timestamp) & (taxi_df['pick_up_time'] < current_timestamp) &
        (taxi_df['drop_off_time'] > start_timestamp) & (taxi_df['drop_off_time'] < current_timestamp)
    ]

    # taxi_df['pick_up_time'] = dd.to_datetime(taxi_df['pick_up_time'], unit='s', errors='coerce')
    # taxi_df['drop_off_time'] = dd.to_datetime(taxi_df['drop_off_time'], unit='s', errors='coerce')

    # 删除时间无法解析的行
    taxi_df = taxi_df.dropna(subset=['pick_up_time', 'drop_off_time'])

    # 规则2：pick_up_time 应当晚于 drop_off_time
    taxi_df = taxi_df[taxi_df['pick_up_time'] < taxi_df['drop_off_time']]

    # 规则3：检查 intersection 是否有效
    taxi_df = taxi_df[taxi_df['pick_up_intersection'].isin(valid_intersections) & 
                      taxi_df['drop_off_intersection'].isin(valid_intersections)]

    # 规则4：起点与终点不能相同
    taxi_df = taxi_df[taxi_df['pick_up_intersection'] != taxi_df['drop_off_intersection']]
    # 按照 pick_up_time 和 drop_off_time 排序
    taxi_df = taxi_df.sort_values(by=['pick_up_time', 'drop_off_time'])
    # 启动进度条
    with ProgressBar():
        # 触发计算并保存清洗后的数据
        cleaned_taxi_df = taxi_df.compute()
        cleaned_taxi_df.to_csv(SAVE_PATH2, index=False)
    
    print("Data cleaning completed.")

def visualize_q2(taxi_trip_count):
    # 打印最大最小值，以及中位数，上下四分位数及对应的id
    print(taxi_trip_count['count'].describe())


    print("drawing histogram...")

    # 根据行程数量排序
    taxi_trip_count = taxi_trip_count.sort_values(by='count', ascending=False).reset_index(drop=True)
    # 获取最大值和最小值对应的 taxi_id 和 count
    max_taxi_id = taxi_trip_count['taxi_id'].iloc[0]
    max_count = taxi_trip_count['count'].iloc[0]

    min_taxi_id = taxi_trip_count['taxi_id'].iloc[-1]
    min_count = taxi_trip_count['count'].iloc[-1]

    # 绘制折线图 X: taxi_id, Y: count
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=taxi_trip_count, x='taxi_id', y='count')
    plt.title('Distribution of the Number of Trips per Taxi')
    plt.xlabel('Taxi ID')
    plt.ylabel('Number of Trips')

    # 在图上用箭头标出最大值和最小值对应的 taxi_id
    plt.annotate(f'Max: {max_count}, Taxi ID: {max_taxi_id}', xy=(max_taxi_id, max_count), xytext=(max_taxi_id, max_count+100), arrowprops=dict(facecolor='red', shrink=0.05))
    plt.annotate(f'Min: {min_count}, Taxi ID: {min_taxi_id}', xy=(min_taxi_id, min_count), xytext=(min_taxi_id, min_count+100), arrowprops=dict(facecolor='red', shrink=0.05))

    plt.show()

def q2():
    # (2) What is the distribution of the number of trips per taxi? Who are the top performers?
    # 计算每辆出租车的行程数量 并作为 csv 文件保存
    with ProgressBar():
        taxi_trip_count = cleaned_taxi_df['taxi_id'].value_counts().compute()
        taxi_trip_count.to_csv(SAVE_PATH3)
    
    # 可视化
    # visualize_q2(taxi_trip_count)

def visualize_q3(daily_trip_count):
    # id,pick_up_date,count
    # 0,2011-01-01,147515
    # 1,2011-01-02,127657

    # 绘制每日行程数量的折线图
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=daily_trip_count, x='pick_up_date', y='count')
    plt.title('Daily Trip Count Throughout the Year')
    plt.xlabel('Date')
    plt.ylabel('Trip Count')
    # MaxNLocator
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(20)) 
    # 旋转 x 轴标签
    plt.xticks(rotation=45)
    plt.show()

def q3():
    # (3) How does the daily trip count (i.e., number of trips per day) change throughout the year? Any rhythm or seasonality?
    with ProgressBar():
        # 1. 从 pick_up_time 中提取日期
        cleaned_taxi_df['pick_up_date'] = dd.to_datetime(cleaned_taxi_df['pick_up_time'], unit='s').dt.date
        # 2. 计算每天的行程数量
        daily_trip_count = cleaned_taxi_df['pick_up_date'].value_counts().compute()
    
    # 按照时间排序
    daily_trip_count = daily_trip_count.sort_index().reset_index()
    # 3. 保存结果
    daily_trip_count.to_csv(SAVE_PATH4)

def q4():
## (4) What is the distribution of the number of departure trips at different locations (i.e., intersections)? What about the distribution of arrival trips? What will you conclude from these two distributions?
    with ProgressBar():
        # 计算每个起点的行程数量
        departure_trip_count = cleaned_taxi_df['pick_up_intersection'].value_counts().compute()
        # 计算每个终点的行程数量
        arrival_trip_count = cleaned_taxi_df['drop_off_intersection'].value_counts().compute()

    departure_trip_count.to_csv(SAVE_PATH5)
    arrival_trip_count.to_csv(SAVE_PATH6)
    print("Data saved.")

def visualize_q4(departure_trip_count, arrival_trip_count):
    # departure_trip_count: id,count
    # 0, 100
    # 1, 200
    # arrival_trip_count: id,count
    # 0, 100
    # 1, 200

    # 降序排序
    departure_trip_count = departure_trip_count.sort_values(by='count', ascending=False).reset_index(drop=True)
    arrival_trip_count = arrival_trip_count.sort_values(by='count', ascending=False).reset_index(drop=True)

    max_departure_id = departure_trip_count['pick_up_intersection'].iloc[0]
    max_departure_count = departure_trip_count['count'].iloc[0]

    max_arrival_id = arrival_trip_count['drop_off_intersection'].iloc[0]
    max_arrival_count = arrival_trip_count['count'].iloc[0]

    # 绘制折线图 在同一张图上绘制出发点和终点的行程数量
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=departure_trip_count, x='pick_up_intersection', y='count', label='Departure')
    sns.lineplot(data=arrival_trip_count, x='drop_off_intersection', y='count', label='Arrival')
    plt.title('Distribution of the Number of Departure and Arrival Trips')
    plt.xlabel('Intersection ID')
    plt.ylabel('Trip Count')
    plt.legend()

    # 在图上用箭头标出最大值对应的 intersection_id
    plt.annotate(f'Max Departure: {max_departure_count}, Intersection ID: {max_departure_id}', xy=(max_departure_id, max_departure_count), xytext=(max_departure_id, max_departure_count+100), arrowprops=dict(facecolor='red', shrink=0.05))
    plt.annotate(f'Max Arrival: {max_arrival_count}, Intersection ID: {max_arrival_id}', xy=(max_arrival_id, max_arrival_count), xytext=(max_arrival_id, max_arrival_count+100), arrowprops=dict(facecolor='red', shrink=0.05))

    plt.show()




if __name__ == '__main__':
    # 使用Dask读取CSV并指定列名
    taxi_df = dd.read_csv(SAVE_PATH1, header=None, names=taxi_columns, on_bad_lines='skip', dtype=taxi_dtypes)
    inter_df = dd.read_csv(PATH2, header=None, names=inter_columns)


    # q1('before')
    # clean(taxi_df, inter_df, SAVE_PATH2)
    cleaned_taxi_df = dd.read_csv(SAVE_PATH2, header = 0 , on_bad_lines='skip', dtype=taxi_dtypes)
    # q1('after')
    # taxi_id,pick_up_time,drop_off_time,pick_up_intersection,drop_off_intersection
    # q2()
    # taxi_trip_count = pd.read_csv(SAVE_PATH3, header= 0) # pandas dataframe
    # visualize_q2(taxi_trip_count)

    # q3()
    # daily_trip_count = pd.read_csv(SAVE_PATH4, header= 0) # pandas dataframe
    # visualize_q3(daily_trip_count)

    # q4()
    departure_trip_count = pd.read_csv(SAVE_PATH5, header= 0) # pandas dataframe
    arrival_trip_count = pd.read_csv(SAVE_PATH6, header= 0) # pandas dataframe
    visualize_q4(departure_trip_count, arrival_trip_count)



    

