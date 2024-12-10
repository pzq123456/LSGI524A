#
## 3.1. Study area（要增加一句关于上海市的共享单车的现状和情况）

本文选取上海市作为研究区域，上海市北界长江，南枕杭州湾，西接江浙两省，东临东海，全市面积 6340.5 平方公里，现辖16个市辖区：黄浦区、徐汇区、长宁区、静安区、普陀区、虹口区、杨浦区、闵行区、宝山区、嘉定区、浦东新、金山区、松江区、青浦区、奉贤区、崇明区。参考第七次全国人口普查主要数据，上海市常住人口为 24870895 人。近几十年来经济飞速发展的同时，上海市逐步形成了多中心、高人口密度及高混杂度的城市格局，这也进一步引起人口拥挤、交通拥堵和环境污染等大城市病。自摩拜单车在上海投放以来，已有13家企业在沪运营，累计投放车辆达到178万辆，其中包括约6万辆互联网租赁电动自行车。

The study area selected in this paper is Shanghai. Shanghai is located in the north of the Yangtze River, the south of Hangzhou Bay, the west of Jiangsu and Zhejiang provinces, and the east of the East China Sea. The total area of the city is 6340.5 square kilometers, and it is under the jurisdiction of 16 districts: Huangpu District, Xuhui District, Changning District, Jing'an District, Putuo District, Hongkou District, Yangpu District, Minhang District, Baoshan District, Jiading District, Pudong New District, Jinshan District, Songjiang District, Qingpu District, Fengxian District, and Chongming District. According to the main data of the seventh national census, the permanent population of Shanghai is 24,870,895. In recent decades, Shanghai has developed rapidly economically and gradually formed a multi-center, high population density, and high complexity urban pattern, which has further caused urban diseases such as population crowding, traffic congestion, and environmental pollution. Since Mobike was put into operation in Shanghai, 13 companies have operated in Shanghai, with a total of 1.78 million vehicles put into operation, including about 60,000 Internet rental electric bicycles.

## 3.2. Datasets and processing

本文的研究用到的数据包括共享单车骑行轨迹数据、上海市基本地理信息数据、上海市兴趣点数据、上海市街景视图数据。

The data used in this paper include shared bicycle riding trajectory data, basic geographic information data of Shanghai, point of interest data of Shanghai, and street view image data of Shanghai.

其中骑行轨迹包括由互联网采集整理得到的 2016 年 8 月 102361 条上海市某品牌共享单车骑行轨迹数据，其包含了一个以“#”分隔的骑行轨迹点集字段，但是由于网络延迟、设备故障等原因该字段内的轨迹点为乱序排列，需要设计算法以恢复正确的骑行轨迹。对于骑行记录数据，按照如下规则清洗：1）去除骑行时长小于1分钟大于 8 小时的骑行记录；2）对于有轨迹点集的数据，去除记录到的轨迹点数量小于 3 个的记录；3）去除存在字段缺失及异常符号的记录；4）去除骑行终点位于上海市之外的记录，该记录超出研究区域。

The riding trajectory data includes 102,361 shared bicycle riding trajectory data of a certain brand in Shanghai in August 2016, which was collected and organized by the Internet. It contains a riding trajectory point set field separated by "#", but due to network delay, equipment failure, etc., the trajectory points in this field are arranged in disorder and need to design an algorithm to restore the correct riding trajectory. For riding record data, the following rules are used for cleaning: 1) Remove riding records with a duration of less than 1 minute and more than 8 hours; 2) For data with trajectory point sets, remove records with less than 3 recorded trajectory points; 3) Remove records with missing fields and abnormal symbols; 4) Remove records with riding endpoints outside Shanghai, which are beyond the study area.

<!-- class_map= {
    0: 'Transportation',
    1: 'Sports and Leisure',
    2: 'Company',
    3: 'Business Residence',
    4: 'Science and Education Culture',
    5: 'Shopping',
    6: 'Scenic Spots',
    7: 'Catering'
} -->

上海市基本地理信息数据包括由 Open  Street  Map 开源地理信息数据网站获取上海市路网数据、兴趣点数据。从 Open Street Map (OSM) 网站下载上海市区域的 OSM 数据，该数据为基于 XML 格式的矢量数据，包含道路、建筑物、兴趣点等地理要素信息，并以节点、关系和区域等形式组织。我们使用 OSMnx 包从 Open Street Map 获取上海市的道路网络数据，包括道路名称、道路等级等信息，并重新投影（CRS: 32651），简化道路网络，生成相应的节点和边。同时，我们还从上海市兴趣点数据集中抽取出八个类别的兴趣点集（交通设施服务、体育休闲服务、公司企业、商务住宅、科教文化服务、购物服务、风景名胜、餐饮服务）共计 122608 条数据。

The basic geographic information data of Shanghai includes road network data and point of interest data of Shanghai obtained from the Open Street Map open geographic information data website. Download the OSM data of the Shanghai area from the Open Street Map (OSM) website. The data is vector data based on XML format, which contains geographical elements such as roads, buildings, and points of interest, and is organized in the form of nodes, relationships, and areas. We use the OSMnx package to obtain road network data of Shanghai from Open Street Map, including road names, road grades, etc., and reproject (CRS: 32651), simplify the road network, and generate corresponding nodes and edges. At the same time, we also extracted eight categories of point of interest sets (Transportation, Sports and Leisure, Company, Business Residence, Science and Education Culture, Shopping, Scenic Spots, Catering) from the point of interest data set of Shanghai, totaling 122,608 data.

## 4.6. Model accuracy

$$
R^2 = 1 - \frac{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{\sum_{i=1}^{n} (y_i - \bar{y})^2}
$$

$$
RMSE = \sqrt{\frac{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{n}}
$$

$$
MAE = \frac{\sum_{i=1}^{n} |y_i - \hat{y}_i|}{n}
$$


## 5.1.1. Cycling temporal characteristics analysis

从时间角度分析共享单车骑行特征，首先统计所有订单的骑行时间及距离，并绘制为柱状图，分析骑行时间和距离的分布规律(fig.a,fig.b)。计算所有订单的平均骑行时间和距离，分析共享单车的骑行特征。可以发现平均骑行距离为1.8公里，一公里左右的短途骑行为主流。可以发现，共享单车平均通勤时长为16分钟，小于10分钟的短途骑行为主流, 极少有人选择骑行一个小时以上。

From the time perspective, the cycling characteristics of shared bicycles are analyzed. First, the riding time and distance of all orders are counted and drawn as a histogram to analyze the distribution law of riding time and distance (fig.a, fig.b). The average riding time and distance of all orders are calculated to analyze the riding characteristics of shared bicycles. It can be found that the average riding distance is 1.8 kilometers, and short rides of about one kilometer are the mainstream. It can be found that the average commuting time of shared bicycles is 16 minutes, and short rides of less than 10 minutes are the mainstream, and very few people choose to ride for more than an hour.

其次，计算同一用户两次骑行之间的时间间隔，绘制时间间隔的累计分布曲线（CDF）及概率密度分布曲线（PDF）。分析统计图（fig.c）累计分布曲线在 200 小时（约间隔 8 天）处具有明显拐点，数据相对集中于该拐点左侧，呈现出明显的短间隔高频特征，即多数用户一周内要多次骑行共享单车。概率密度分布曲线数（fig.d）据相对集中于短间隔方向（ 间隔 100 小时以下 ），这也意味着大部分用户频繁使用共享单车，两次骑行间隔较短，多用于日常通勤。

Secondly, calculate the time interval between two rides of the same user, and draw the cumulative distribution curve (CDF) and probability density distribution curve (PDF) of the time interval. Analyze the cumulative distribution curve in the statistical chart (fig.c), the cumulative distribution curve has an obvious inflection point at 200 hours (about 8 days), and the data is relatively concentrated on the left side of the inflection point, showing an obvious short interval high-frequency feature, that is, most users need to ride shared bicycles multiple times a week. The probability density distribution curve (fig.d) is relatively concentrated in the short interval direction (interval below 100 hours), which also means that most users frequently use shared bicycles, and the interval between two rides is short, mostly used for daily commuting.

最后，对共享单车通勤时段进行汇总分析，研究不同工作日一天二十四小时不同时段的通勤规律。首先将骑行数据的开始时间按照工作日分组汇总，再对每一个工作日按二十四小时统计每一个小时内的订单数量，最后将每个小时的订单数量除以当前工作日的总订单数量，得到每个小时的订单占比。分析统计图（fig.e）可以发现，工作日骑行具有明显的早晚高峰特征，早高峰集中在8:00至9:00，晚高峰则以16:00至17:00较为突出，与用户工作日上班、上学等通勤需求贴合。周末骑行曲线总体平缓，且8:00至15:00总体高于工作日，其中16:00至19:00呈现出一个平滑单峰，这样的分布与用户周末休闲放松需求相符合。

Finally, summarize and analyze the commuting time of shared bicycles, and study the commuting rules of different working days in different time periods of twenty-four hours. First, summarize the start time of the riding data according to the working day, then count the number of orders in each hour within twenty-four hours for each working day, and finally divide the number of orders in each hour by the total number of orders of the current working day to obtain the proportion of orders in each hour. Analyze the statistical chart (fig.e), it can be found that weekday riding has obvious morning and evening peak characteristics. The morning peak is concentrated from 8:00 to 9:00, and the evening peak is more prominent from 16:00 to 17:00, which is in line with the commuting needs of users on weekdays. The weekend riding curve is generally flat, and 8:00 to 15:00 is generally higher than weekdays. Among them, 16:00 to 19:00 shows a smooth single peak, which is in line with the user's weekend leisure and relaxation needs.

## 5.1.2. Cycling spatial characteristics analysis
从空间角度，分析共享单车骑行特征，首先使用兴趣点匹配算法（Algorithm 2）为骑行轨迹终点匹配兴趣点类别，绘制饼图分析骑行目的地类别的分布。分析统计图（fig.f）可以发现购物服务、交通设施服务和餐饮服务为主要目的地，占比近六成，反映了上海市商业活动活跃、交通发达、生活便利的特点。科教文化服务、商务住宅和公司企业也是较多用户的选择，占比近三成，表明上海市拥有较多较密集的院校及企业。风景名胜和体育休闲服务占比最少，可能与人口密集、生活压力大有关。

From the spatial perspective, analyze the cycling characteristics of shared bicycles. First, use the interest point matching algorithm (Algorithm 2) to match the interest point category for the end point of the riding trajectory, draw a pie chart to analyze the distribution of riding destination categories. Analyze the statistical chart (fig.f), it can be found that Shopping, Transportation, and Catering are the main destinations, accounting for nearly 60%, reflecting the characteristics of active commercial activities, developed transportation, and convenient life in Shanghai. Science and Education Culture, Business Residence, and Company are also choices for many users, accounting for nearly 30%, indicating that Shanghai has many and dense schools and companies. Scenic Spots and Sports and Leisure services account for the least, which may be related to the dense population and high life pressure.



## References
1. Shanghai Municipal Government. (2024). Guidelines for Encouraging and Regulating the Development of Internet Rental Bicycles in Shanghai (Trial). Shanghai Government. https://www.shanghai.gov.cn/
