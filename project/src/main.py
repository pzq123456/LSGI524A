import pickle
import pandas as pd
import transbigdata
from leuvenmapmatching.matcher.distance import DistanceMatcher
from leuvenmapmatching.map.inmem import InMemMap
import osmnx as ox
import time
from shapely.ops import unary_union
import geopandas as gpd
from shapely.geometry import Point

import os
from tqdm import tqdm

from log import get_logger, save_checkpoint

PATH = os.path.dirname(os.path.abspath(__file__))

PATH1 = os.path.join(PATH, '../', 'data', 'bike162.csv')
PATH2 = os.path.join(PATH, '../', 'data', 'track16.pickle')

SAVE_PATH = os.path.join(PATH, '../', 'output', 'StreetMatching')

FILENAME = 'ID_${id}.shp' # 文件名模板

# 设置超时时间和使用缓存
# ox.settings.timeout = 180
ox.settings.timeout = 180
ox.settings.retry_on_timeout = True
ox.settings.use_cache = True

# 辅助函数：将秒转换为小时:分钟:秒
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

# 自定义函数来获取路网，支持重试
def get_graph_with_retry(north, south, east, west, retries=6, wait=6):
    """
    尝试从 OSM 获取路网数据，如果失败则重试。
    :param north: 北边界
    :param south: 南边界
    :param east: 东边界
    :param west: 西边界
    :param retries: 重试次数
    :param wait: 重试前等待的时间（秒）
    :return: OSMnx 图
    """
    for attempt in range(retries):
        try:
            # 尝试获取路网
            return ox.graph_from_bbox(north, south, east, west, network_type='bike', simplify=False)

        except Exception as e:
            # print(f"获取路网数据失败，尝试 {attempt + 1}/{retries}. 错误: {e}")
            # time.sleep(wait)  # 等待后重试
            logger.error(f"获取路网数据失败，尝试 {attempt + 1}/{retries}. 错误: {e}")
            time.sleep(wait)
    raise RuntimeError("无法获取路网数据，已达到最大重试次数。")

# 修改后的 process_id 函数
def process_id(id, df):
    # print(f"开始处理 ID: {id}")
    try:
        # 开始本次循环的时间
        loop_start = time.time()
        logger.info(f"开始处理 ID: {id}")

        # print(f"开始处理 ID: {id}")
        track_points = df.loc[id]

        # 过滤掉 None 值
        track_points_filtered = track_points.dropna()

        # 生成 DataFrame，包含 lon 和 lat 列
        track_df = pd.DataFrame(track_points_filtered.tolist(), columns=['lon', 'lat'])
        track_df['Lng84'], track_df['Lat84'] = transbigdata.gcj02towgs84(track_df['lon'], track_df['lat'])

        # 创建 geometry 列，将经纬度转换为 Point 对象
        track_df['geometry'] = track_df.apply(lambda row: Point(row['Lng84'], row['Lat84']), axis=1)
        gdf = gpd.GeoDataFrame(track_df, geometry='geometry')
        gdf.set_crs(epsg=4326, inplace=True)

        # 获得边界和轨迹点
        bound = gdf.total_bounds  # 返回 (minx, miny, maxx, maxy)
        gdf = gdf.to_crs(32651)
        path = list(zip(gdf.geometry.y, gdf.geometry.x))

        # 在请求之前暂停 2 秒，避免过多请求
        time.sleep(2)

        # 获取路网，增加重试机制
        bounds = bound
        north, south, east, west = bounds[3] + 0.005, bounds[1] - 0.005, bounds[2] + 0.005, bounds[0] - 0.005
        G = get_graph_with_retry(north, south, east, west)

        # 投影到指定的 CRS
        G_p = ox.project_graph(G, to_crs=32651)
        G_simplified = ox.simplify_graph(G_p)
        G_consolidated = ox.consolidate_intersections(G_simplified, tolerance=15, dead_ends=False)

        # 将简化后的路网转换为 GeoDataFrames
        nodes_p, edges_p = ox.graph_to_gdfs(G_consolidated, nodes=True, edges=True)

        # 构建网络
        map_con = InMemMap(name='pNEUMA', use_latlon=False)
        for node_id, row in nodes_p.iterrows():
            map_con.add_node(node_id, (row['y'], row['x']))
        for node_id_1, node_id_2, _ in G_consolidated.edges:
            map_con.add_edge(node_id_1, node_id_2)

        # 构建地图匹配工具
        matcher = DistanceMatcher(
            map_con=map_con, obs_noise=50, max_dist=500, min_prob_norm=0.001,
            non_emitting_states=True, non_emitting_length_factor=0.85,
            max_lattice_width=50, avoid_goingback=True, dist_noise=50
        )
        states, _ = matcher.match(path, unique=False)

        # Obtain the path GeoDataFrame
        pathdf = pd.DataFrame(matcher.path_pred_onlynodes, columns=['u'])
        pathdf['v'] = pathdf['u'].shift(-1)
        pathdf = pathdf[-pathdf['v'].isnull()]
        pathgdf = pd.merge(pathdf, edges_p.reset_index())
        pathgdf = gpd.GeoDataFrame(pathgdf)

        # 合并所有的 geometry 到一个单一的 MultiLineString
        merged_geometry = unary_union(pathgdf.geometry)
        merged_pathgdf = gpd.GeoDataFrame({'ID': id, 'geometry': [merged_geometry]}, crs=pathgdf.crs)

        # 动态生成文件名，使用 ID 值
        # shapefile_path = rf'D:\桌面\Semester1 24-25\URBAN AND GEOSPATIAL BIG DATA ANALYTICS (LSGI524A)\Project\StreetMatching\ID_{id}.shp'
        # merged_pathgdf.to_file(shapefile_path, driver='ESRI Shapefile')
        # print(f"Shapefile 已成功保存为: {shapefile_path}")
        # 保存为 shapefile
        merged_pathgdf.to_file(getSavePath(id), driver='ESRI Shapefile')
        # print(f"Shapefile 已成功保存为: {getSavePath(id)}")
        # 保存成功后记录到日志
        logger.info(f"Shapefile 已成功保存为: {getSavePath(id)}")
        # save_checkpoint
        save_checkpoint(f"{id}", 'success')

        # 计算本次循环的结束时间
        loop_end = time.time()

        # 本次循环用时
        this_loop_duration = loop_end - loop_start
        # print(f"ID: {id} 用时: {format_time(this_loop_duration)}")
        # print("-" * 40)
        logger.info(f"ID: {id} 用时: {format_time(this_loop_duration)}")

    except Exception as e:
        # print(f"处理 ID: {id} 时出错: {e}")
        logger.error(f"处理 ID: {id} 时出错: {e}")
        # save_checkpoint
        save_checkpoint(f"{id}", 'failed')


def getSavePath(id):
    FOLDER = os.path.join(SAVE_PATH, str(id))
    if not os.path.exists(FOLDER):
        os.makedirs(FOLDER)
    return os.path.join(SAVE_PATH, str(id), FILENAME.replace('${id}', str(id)))

def test():
    # 测试文件路径
    print(PATH1)
    print(PATH2)

    ID = 70000
    # print save path
    print(SAVE_PATH)
    # print file name
    print(FILENAME.replace('${id}', str(ID)))
    # print file path
    print(os.path.join(SAVE_PATH, FILENAME.replace('${id}', str(ID))))


# 读取原始数据和 pickle 文件
if __name__ == "__main__":
    logger = get_logger()

    originData = pd.read_csv(PATH1)

    with open(PATH2, 'rb') as file:
        data = pickle.load(file)
    
    df = pd.DataFrame(data).iloc[:, 1:]

    # process_id(70000, df)

    total_iterations = 97867 - 70000 + 1

    for i in tqdm(range(70000, 97867 + 1)):
        process_id(i, df)
