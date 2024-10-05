import bz2
import os
import dask.dataframe as dd
# import progressbar in dask
from dask.diagnostics import ProgressBar

# ./data/
PARENT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data') # path to data directory
PATH1 = os.path.join(PARENT_PATH, 'taxi_id.csv.bz2') # path to the zipped file

SAVE_PATH1 = os.path.join(PARENT_PATH, 'taxi_id.csv') # path to the unzipped file

def peek_data():
    # peek the data
    # 仅仅加载前 5 行数据 以供查看
    with bz2.open(PATH1, 'rt') as f:
        for i in range(5):
            print(f.readline())

if __name__ == '__main__':
    # peek the data
    peek_data()