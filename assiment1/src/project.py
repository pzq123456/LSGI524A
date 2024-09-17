import dask.dataframe as dd
import pandas as pd
from pyproj import Transformer
from dask.diagnostics import ProgressBar

transformer = Transformer.from_crs("EPSG:4326", "EPSG:26916", always_xy=True)

# PARENT_PATH = 'LSGI524A/assiment1' # linux path
PARENT_PATH = 'G:/polyulessons/LSGI524A/assiment1' # windows path

SAVE_PATH3 = PARENT_PATH + '/data/locations.csv'
SAVE_PATH4 = PARENT_PATH + '/data/output.csv'


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

getProjectedDistance(SAVE_PATH3, SAVE_PATH4)
