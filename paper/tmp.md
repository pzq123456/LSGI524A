## 4.1. Cycling track reorder and map matching

Figure 3是对一段骑行轨迹进行重排序和路网匹配流程的示意图。可以发现原始轨迹数据具有明显的“跳跃现象”，即相邻的轨迹点之间的距离可能会很远。这个问题可以用一个很简单的思路来解决，即认为最近的点大概率是下一个点。

Figure 3 is a schematic diagram of the reordering and road network matching process of a cycling trajectory. It can be seen that the original trajectory data has an obvious "jump phenomenon", that is, the distance between adjacent trajectory points may be very far. This problem can be solved with a very simple idea, that is, the nearest point is probably the next point.

对于乱序轨迹点集，在知道始末点的前提下，本文提出了一种基于 GeoHash 空间索引及曼哈顿距离及贪婪策略轨迹重排序算法（Figure 4a）:认为所有记录中的轨迹点集都是乱序状态，对于任意一轨迹点集，首先创建空列表 List 并将包含了起点和终点的所有点组成的列表 Pn 逐点计算 GeoHash 编码并放入集合 GeoHash 中（该步骤同时借助集合的特性实现了去重复）。然后，循环迭代，直到轨迹点列表为空。在每次迭代中，算法会计算当前点与轨迹末尾点的曼哈顿距离，并找到距离最近的点。如果找到的最近点就是终点，则算法终止，否则将最近点加入轨迹并从 GeoHash 集合中删除。最后，将轨迹列表 List 中的 GeoHash 编码转换为坐标并返回简化后的轨迹。

For the unordered trajectory point set, under the premise of knowing the starting and ending points, this paper proposes a trajectory reordering algorithm based on GeoHash spatial index, Manhattan distance, and greedy strategy (Figure 4a): it is assumed that all trajectory point sets in the records are in a disordered state. For any trajectory point set, first create an empty list List and calculate the GeoHash encoding for each point in the list Pn containing all points of the starting and ending points and put it into the set GeoHash (this step also uses the characteristics of the set to achieve deduplication). Then, loop iteratively until the trajectory point list is empty. In each iteration, the algorithm calculates the Manhattan distance between the current point and the end point of the trajectory and finds the nearest point. If the nearest point found is the end point, the algorithm terminates, otherwise, the nearest point is added to the trajectory and removed from the GeoHash set. Finally, convert the GeoHash encoding in the trajectory list List to coordinates and return the simplified trajectory.

由于 Python 编程语言的集合（Set）原生的散列值计算函数作用于元组（tuple）类型的数据时会发生二进制精度损失，所以需要首先使用 GeoHash 算法对位置元组进行编码（encode）再将得到的字符串存入集合中，在需要用到实际坐标时再使用对应的解码方法（decode），这样可以规避使用存入及去除集合时由于散列值计算带来的精度损失。考虑到 GeoHash 编码存在距离失真的问题，本算法使用两经纬度坐标间的曼哈顿距离来估算实际距离。

Since the native hash value calculation function of the set in the Python programming language acts on the data of the tuple type, there will be binary precision loss, so it is necessary to first encode (encode) the position tuple using the GeoHash algorithm and then store the obtained string in the set. When the actual coordinates are needed, use the corresponding decoding method (decode) to avoid the precision loss caused by the hash value calculation when storing and removing the set. Considering the distance distortion problem of GeoHash encoding, this algorithm uses the Manhattan distance between the two longitude and latitude coordinates to estimate the actual distance.

最后，利用OSMnx包构建了包含骑行道路节点和边的拓扑网络。将排序后的GPS轨迹使用修改的隐马尔可夫模型（HMM）进行地图匹配，通过计算发射和转移概率，利用维特比算法选择最可能的路径，最终得到匹配后的共享单车骑行轨迹。

Finally, using the OSMnx package to construct a topological network containing riding road nodes and edges. The sorted GPS trajectory is matched to the map using a modified Hidden Markov Model (HMM). By calculating the emission and transition probabilities, the Viterbi algorithm is used to select the most likely path, and the matched shared bicycle riding trajectory is finally obtained.



Figure 3. Schematic of the cycling trajectory reordering and road network matching process


## 4.2. Cycling destination recognition

在拥有了轨迹数据后，我们还希望进一步探索用户的骑行目的地，以分析动机。这里我们想到使用兴趣点匹配算法，即将轨迹终点与兴趣点进行匹配，以确定用户的骑行目的地类别。有两个关键思想使得我们的算法具有实际意义。首先，地理学第一定律：事物都是彼此相关的，但是距离越近，相关性越大。其次，共享单车很好地解决了“最后一公里”问题，即用户骑行共享单车会尽可能地靠近目的地，而不像公共交通那样只能到达固定的站点。

考虑到该算法涉及到地数据量非常巨大。我们有大约12万个兴趣点，有10万条轨迹数据。想要处理这么多数据，而不考虑优化算法地性能是一件非常可怕地事情：如果直接对所有点进行暴力搜素，算法时间复杂度约为 $O(n^2)$，粗略估计将执行120亿次距离计算（haversine）。据本机（i7-10870H,RAM 16 GB）测算，执行一次大约消耗 15 μs，粗略估计，在不考虑排序操作的情况下，算法将执行超过三小时，因此需要建立用于支持高效查找的空间数据结构。

2008年 Gustavo Niemeyer 提出了 GeoHash 地理编码系统，它能将地理位置编码成由字母和数字组成的短字符串。GeoHash 是一种多层级的空间数据结构，通过网格状的划分及 Z 形空间填充曲线 (Z-order curve)方式将空间进行编码。GeoHash 编码精度可以通过增加编码字符长度无限拓展，同时可以通过去除编码末尾的字符来降低精度 (空间精度随之降低)。由于其编码结构具有层级性，GeoHash 保证了两个共享前缀越长的编码，其代表的地理位置越接近。

综上，我们可以概括GeoHash 编码有两个关键特性：1. 编码长度越长，精度越高；2. 编码前缀相的部分越长，表示地理位置越接近。我们可以利用这两个特性，将空间查询动作转化为字符串匹配问题。（Figure 4e）

该算法首先对兴趣点数据集构建树形索引（GeoHashTree）（Figure 4c,d），而后对某一个轨迹终点执行逐步扩大搜索空间范围的贪心算法（greedyQuery）。贪心搜索算法（Figure 4b）对输入编码字符串首先执行一次搜索操作，若未得到返回值，就会逐个去除最后一位（扩大空间范围）并再次搜索，直到找到最邻近的兴趣点（或者待匹配编码为空）。高效的空间索引大大加快了最邻近查找的速度，经试验，在十二万条兴趣点数据集中使用该算法对近十万条轨迹数据的终点进行最邻近匹配共耗费约两分钟。

这种高效算法能够给科研工作带来一定的便利，因此是有价值的。在某些情况下，这种优化算法甚至是决定性的。例如，我们可以使用该算法对轨迹中的每一个点进行兴趣点匹配，从而将用户的骑行轨迹从地理坐标转化为由系列兴趣点类别编码组成的序列（句子），并深入分析用户行为。若不进行优化，这种分析过程会被视为不切实际的。


### 3.2.2 轨迹重排序及长度量测


计算 GeoHash 首先需要将经纬度坐标分别转换为二进制表示。然后按照“经度值占偶数位，纬度值占奇数位”的规则将经纬度交织为一个二进制串，最后使用 Base32 编码转换为字符串。GeoHash 算法的计算过程可以概括为以下公式：

$$GeoHash(lon, lat) = Base32(Interleave(Binary(lon), Binary(lat)))$$

其中，Interleave 函数表示经纬度二进制值的交织操作，Base32 函数表示二进制值转换为 Base32 编码的操作。

![](../imgs/c3/geohash.png)

曼哈顿距离由纽约市曼哈顿的棋盘式街道布局而得名，定义为两个点的坐标轴投影长度之。在二维平面上，两点 (x1, y1) 和 (x2, y2) 之间的曼哈顿距离为：

$$d(x, y) = |x_1 - y_1| + |x_2 - y_2|$$

考虑到轨迹点密度较高，相邻点之间的距离很短，且经纬度变化范围较小（绝大部分相邻点之间的经纬度跨度不超过0.001°），因此曼哈顿距离能够有效捕捉轨迹点的局部运动特征。且曼哈顿距离的计算公式简单，仅涉及绝对值运算，计算效率高。对于具有大量轨迹点的GPS数据，使用曼哈顿距离可以显著降低计算成本。因此，本算法通过计算两个坐标点之间的曼哈顿距离来判断两个点之间实际的空间距离。

| 经度 | 纬度 |
| -- | -- |
|121.347|31.392|
|121.348|31.389|
|121.349|31.390|
|121.350|31.390|
| ... | ... |

对于乱序轨迹点集，在知道始末点的前提下，本文提出了一种基于 GeoHash 空间索引及曼哈顿距离及贪婪策略轨迹重排序算法:认为所有记录中的轨迹点集都是乱序状态，对于任意一轨迹点集，首先创建空列表 List 并将包含了起点和终点的所有点组成的列表 Pn 逐点计算 GeoHash 编码并放入集合 GeoHash 中（该步骤同时借助集合的特性实现了去重复）。然后，循环迭代，直到轨迹点列表为空。在每次迭代中，算法会计算当前点与轨迹末尾点的曼哈顿距离，并找到距离最近的点。如果找到的最近点就是终点，则算法终止，否则将最近点加入轨迹并从 GeoHash 集合中删除。最后，将轨迹列表 List 中的 GeoHash 编码转换为坐标并返回简化后的轨迹。

![](../imgs/3.3-2.png)

由于 Python 编程语言的集合（Set）原生的散列值计算函数作用于元组（tuple）类型的数据时会发生二进制精度损失，所以需要首先使用 GeoHash 算法对位置元组进行编码（encode）再将得到的字符串存入集合中，在需要用到实际坐标时再使用对应的解码方法（decode），这样可以规避使用存入及去除集合时由于散列值计算带来的精度损失。考虑到 GeoHash 编码存在距离失真的问题，本算法使用两经纬度坐标间的曼哈顿距离来估算实际距离。以下是对某一真实路径进行排序的实际效果：

![](../imgs/c3/轨迹排序.png)

假设地球是一个球体，球面半径为 r（取 6371000 米），用经度 lon 和纬度 lat 表示球面上的点，则在已知有序骑行轨迹 n 个点组成的列表($List = [(lon1, lat1), (lon2, lat2), \cdots, (lonn, latn)]$)的情况下，可以使用 Haversine 算法计算得每段子轨迹的长度再累加得总轨迹长度。

$$List = [(lon1, lat1), (lon2, lat2), \cdots, (lonn, latn)]$$

$$d = \sum_{i=1}^{n-1} 2r \arcsin(\sqrt{\sin^2(\frac{lat_{i+1} - lat_i}{2}) + \cos(lat_i) \cos(lat_{i+1}) \sin^2(\frac{lon_{i+1} - lon_i}{2})})$$

使用上述方法对一段轨迹进行处理，计算得轨迹起点与终点间的直接半正弦距离为 2118.25 米，未排序轨迹点集的累计半正弦距离（认为地球半径为 6371000 米）为 8685.89 米，经过算法重排序后的累计半正弦距离为 3605.04 米。可以发现，由于未经处理的轨迹点集中存在部分不合理的乱序点，导致轨迹总长度明显偏大，经算法重排序后的轨迹点集较为合理。在中央处理器为 i7-10870H，机带RAM 16GB 的 Windows11 笔记本上，使用该算法处理十万条轨迹数据总耗时约1小时31分。


## 6. Discussions and conclusions: 

This study reconstructed large-scale cycling trajectories and calculated cycling volumes at the street level during four different time periods, revealing the spatiotemporal patterns and trends of shared bicycle usage. A Random Forest regression model was employed to analyze the impact of various factors and their nonlinear effects on cycling volumes. The results showed that: 

(1) 共享单车的骑行模式呈现出明显的时间特征，工作日和周末的骑行模式存在显著差异。工作日骑行高峰期为早晚高峰，周末骑行高峰期为下午。

(2) 共享单车是典型的短途出行工具，骑行距离两公里以下骑行时长一分钟以下的短途骑行为主流。大部分用户两次骑行间隔较短，多用于日常通勤。购物服务、交通设施服务和餐饮服务为主要目的地，占比近六成。

