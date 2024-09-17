# Assiment 1 

## 性能优化
根据测试，每次坐标投影操作约需 0.02 秒，对于包含两万多条记录的完整数据集，顺序执行预计需要约 400 秒（即不到 7 分钟）。为了提升性能，我采用了两种优化手段：分块并行计算和向量化处理。首先，分块并行计算通过 dask 框架实现，dask 可以将大规模数据集自动划分为多个分块，并利用多核 CPU 并行执行任务，从而显著提高计算效率。其次，频繁的 I/O 操作会拖慢整体性能，因此我采用向量化计算，通过一次性加载大批数据，并对整个数据集进行批量操作。pyproj 底层基于 proj4，能够支持 ndarray 的向量化处理，从而进一步加速了坐标投影过程，大幅减少了逐行计算的开销。通过这两种方法，数据处理的效率得到了显著提升，最终执行时间缩短到 4.92 秒。

Based on testing, each coordinate projection takes approximately 0.02 seconds. For a dataset with over 20,000 records, sequential processing would take around 400 seconds (nearly 7 minutes). To improve performance, I applied two optimization techniques: parallel processing and vectorization. 

First, parallel processing was implemented using the `dask` framework, which splits large datasets into smaller chunks and utilizes multiple CPU cores for parallel execution, significantly boosting efficiency. Second, frequent I/O operations can slow down performance, so I used vectorization to load large batches of data at once and perform operations on the entire dataset simultaneously. The `pyproj` library, built on `proj4`, supports `ndarray`-based vectorization, further accelerating the projection process by reducing the overhead of row-by-row computation.

These methods reduced the total execution time to 4.92 seconds.

## pre-processing

## data analysis

## visualization

## clustering