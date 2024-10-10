import os
import dask.dataframe as dd
from dask.diagnostics import ProgressBar
import pandas as pd

# ./data/
PARENT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data') # path to data directory
PATH1 = os.path.join(PARENT_PATH, 'taxi_id.csv.bz2') # path to the zipped file
PATH2 = os.path.join(PARENT_PATH, 'intersections.csv') # path to the zipped file

SAVE_PATH1 = os.path.join(PARENT_PATH, 'taxi_id.csv') # path to the unzipped file
SAVE_PATH2 = os.path.join(PARENT_PATH, 'taxi_id_clean.csv') # path to the unzipped file

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
def q1():
    with ProgressBar():
        print(f'Number of unique taxis: {taxi_df["taxi_id"].nunique().compute()}')
        print(f'Number of trips recorded: {taxi_df["taxi_id"].count().compute()}')

def clean(taxi_df, inter_df, SAVE_PATH2):
    valid_intersections = set(inter_df['id'])

    taxi_df = taxi_df.dropna()
    taxi_df = taxi_df.drop_duplicates()

    # 规则1：检查时间格式是否为有效的 Unix 时间
    current_timestamp = pd.Timestamp.now().timestamp()  # 获取当前 Unix 时间戳
    taxi_df = taxi_df[
        (taxi_df['pick_up_time'] > 0) & (taxi_df['pick_up_time'] < current_timestamp) &
        (taxi_df['drop_off_time'] > 0) & (taxi_df['drop_off_time'] < current_timestamp)
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


if __name__ == '__main__':
    # 使用Dask读取CSV并指定列名
    taxi_df = dd.read_csv(SAVE_PATH1, header=None, names=taxi_columns, on_bad_lines='skip', dtype=taxi_dtypes)
    inter_df = dd.read_csv(PATH2, header=None, names=inter_columns, )
    # q1()
    clean(taxi_df, inter_df, SAVE_PATH2)

    

