import os
import pandas as pd
from collections import defaultdict
import tqdm
import pickle

DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(DIR, 'simple', 'class')
PATH1 = os.path.join(DATA_DIR, 'poi_geohash.csv')
# paper\src\simple\class\tmp\geohash_tree.pkl
PATH2 = os.path.join(DATA_DIR, 'tmp', 'geohash_tree.pkl')

def geohashTree(data):
    # 初始化一个字典来存储每一位的字符集
    char_sets = defaultdict(set)

    # 遍历每个Geohash，统计每一位的字符
    for geohash in tqdm.tqdm(data['geohash']):
        for i, char in enumerate(geohash):
            char_sets[i].add(char)

    # 输出每一位的字符集大小
    for i, chars in char_sets.items():
        print(f"位 {i}: {len(chars)} 种字符")
    
    geohash_counts = data['geohash'].value_counts()
    print(geohash_counts.describe())


def read_Tree(path):
    with open(path, 'rb') as f:
        tree = pickle.load(f)
    return tree

if __name__ == '__main__':
    # read data
    # data = pd.read_csv(PATH1)
    # print(data.head())
    #     class         lon        lat       geohash
    # 0      0  121.180367  31.161415  wtw1m8bb7hyc
    # 1      0  121.166489  31.173580  wtw1m4yxrbd8
    # 2      0  121.153336  31.164995  wtw1kcmjm24u
    # 3      0  121.193138  31.151411  wtw1jyfnhgcs
    # 4      0  121.177567  31.227278  wtw1tkyb1fwc

    # 计算geohash

    # geohashTree(data)

    # read tree
    tree = read_Tree(PATH2)
    topology, filter_effect = tree.get_tree_topology_with_filter()
    print(topology)
    
    with open(os.path.join(DATA_DIR, 'tmp', 'filter_effect.txt'), 'w') as f:
        f.write(str(filter_effect))




