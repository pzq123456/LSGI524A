import bz2
import datetime
import os

from dask.diagnostics import ProgressBar

import dask
from dask import delayed

# 1,1293840000,1293840848,952,2021

# 2,1293840001,1293840523,1372,2815

# 3,1293840003,1293840276,856,1149

# 4,1293840004,1293840299,2060,1956

# 5,1293840007,1293841159,2506,1332

times = [
    1293840000,
    1293840001,
    1293840003,
    1293840004,
    1293840007
]

# 处理 unix time
def unix2time(x):
    return datetime.datetime.fromtimestamp(x)

def time2unix(x):
    return datetime.datetime.timestamp(x)

# 解压缩单个 bz2 文件的函数
def decompress_bz2_chunk(source_path, chunk_start, chunk_size, target_path):
    with bz2.open(source_path, 'rb') as f_in:
        # 移动到指定的起始位置
        f_in.seek(chunk_start)
        chunk = f_in.read(chunk_size)
        with open(target_path, 'ab') as f_out:  # 追加写入
            f_out.write(chunk)

# 获取文件大小并分块
def chunk_file(file_path, chunk_size=1024*1024*10):  # 默认10MB分块
    file_size = os.path.getsize(file_path)
    return [(offset, min(chunk_size, file_size - offset)) 
            for offset in range(0, file_size, chunk_size)]

# 并行处理 bz2 解压缩
def parallel_decompress_bz2(source_path, target_path, chunk_size=1024*1024*10):
    # 分块文件
    chunks = chunk_file(source_path, chunk_size)

    # 延迟计算任务，处理每个块
    tasks = [delayed(decompress_bz2_chunk)(source_path, chunk_start, chunk_size, target_path) 
             for chunk_start, chunk_size in chunks]
    with ProgressBar():
        # 执行任务并并行计算
        dask.compute(*tasks)

def unzipbz2(PATH, SAVE_PATH):
    # 并行解压缩
    parallel_decompress_bz2(PATH, SAVE_PATH)

if __name__ == '__main__':
    for t in times:
        print(unix2time(t))
