# 讲稿 LSGI524A Final Report 29/11/2024
## From the time perspective （16）

1. 骑行时间距离分布：统计所有订单的骑行时间及距离，并绘制为柱状图，分析骑行时间和距离的分布规律。
1. Distribution of riding time and distance: Statistics of the riding time and distance of all orders, and draw them as a histogram to analyze the distribution law of riding time and distance.
2. 用户骑行时间间隔分布：计算同一用户两次骑行之间的时间间隔，绘制时间间隔的概率密度分布曲线。
2. Distribution of time interval between two rides of the same user: Calculate the time interval between two rides of the same user and draw the probability density distribution curve of the time interval.
3. 一周七天逐小时订单数量：按照一周七天和24小时分组，统计每小时的订单数量，绘制归一化折线图，分析订单数量的分布规律。
3. Order count per hour for seven days a week: Grouped by seven days a week and 24 hours, count the number of orders per hour, draw a normalized line chart, and analyze the distribution law of the number of orders.

## 
可以发现平均骑行距离为1.8公里，一公里左右的短途骑行为主流。

We can find that the average riding distance is 1.8 kilometers, and short rides of about one kilometer are the mainstream.

可以发现，共享单车平均通勤时长为16分钟，小于10分钟的短途骑行为主流。

It can be found that the average commuting time of shared bicycles is 16 minutes, and short rides of less than 10 minutes are the mainstream.

## 
工作日骑行具有明显的早晚高峰特征，早高峰集中在8:00至9:00，晚高峰则以16:00至17:00较为突出，与用户工作日上班、上学等通勤需求贴合。

Weekday riding has obvious morning and evening peak characteristics. The morning peak is concentrated from 8:00 to 9:00, and the evening peak is more prominent from 16:00 to 17:00, which is in line with the commuting needs of users on weekdays.

周末骑行曲线总体平缓，且8:00至15:00总体高于工作日，其中16:00至19:00呈现出一个平滑单峰，这样的分布与用户周末休闲放松需求相符合。

The weekend riding curve is generally flat, and 8:00 to 15:00 is generally higher than weekdays. Among them, 16:00 to 19:00 shows a smooth single peak, which is in line with the user's weekend leisure and relaxation needs.
## 

数据相对集中于短间隔方向（ 间隔 100 小时以下 ），这也意味着大部分用户频繁使用共享单车，两次骑行间隔较短，多用于日常通勤.

The data is relatively concentrated in the short interval direction (interval below 100 hours), which also means that most users frequently use shared bicycles, and the interval between two rides is short, which is mostly used for daily commuting.

## From the space perspective

1. 骑行目的地分布：使用兴趣点匹配算法（Algorithm 2）为骑行轨迹终点匹配兴趣点类别，绘制饼图分析骑行目的地类别的分布。
2. Distribution of riding destinations: Use the interest point matching algorithm (Algorithm 2) to match the interest point category for the end point of the riding trajectory, draw a pie chart to analyze the distribution of riding destination categories.
3. 路网骑行量匹配分析：将骑行轨迹匹配到路网，提取每条街道的骑行量。
4. Riding road matching analysis: Match the riding trajectory to the road and extract the cycling volume for each street.


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


购物服务、交通设施服务和餐饮服务为主要目的地，占比近六成，反映了上海市商业活动活跃、交通发达、生活便利的特点。

Shopping(5), Transportation(0), and Catering(7) are the main destinations, accounting for nearly 60%, reflecting the characteristics of active commercial activities, developed transportation, and convenient life in Shanghai.

科教文化服务、商务住宅和公司企业也是较多用户的选择，占比近三成，表明上海市拥有较多较密集的院校及企业。风景名胜和体育休闲服务占比最少，可能与人口密集、生活压力大有关。

Science and Education Culture(4), Business Residence(3), and Company(2) are also choices for many users, accounting for nearly 30%, indicating that Shanghai has many and dense schools and companies. Scenic Spots(6) and Sports and Leisure(1) services account for the least, which may be related to the dense population and high life pressure.


## 
在此研究中，依据骑行轨迹的起始时间，将依赖变量和解释变量构建在街道尺度上。
In this study, dependent and explanatory variables were created at the street level.

考虑到不同时段骑行的时空模式存在差异（图2），本研究依据骑行起始时间的逐小时统计结果，划分了四个不同的分析模型。选取的时间段分别为工作日高峰、工作日非高峰、休息日高峰与休息日非高峰。其中工作日高峰时段为7时至9时与17时至20时，非高峰时段为剩余时段。周末没有呈现明显的高低峰，因此将周末视为一个整体时段。提取各个时段骑行轨迹的重叠计数，得到街道尺度的骑行量如图1所示。

Extract the overlap count of riding trajectories in each period to obtain the riding volume at the street level as shown in Figure 1. In this study, dependent and explanatory variables were created at the street level. Considering that there are differences in the spatiotemporal patterns of riding at different times (Figure 2), this study divided the analysis into four different models based on the hourly statistical results of the riding start time. 

The selected time periods are workday peak, workday off-peak, weekend peak, and weekend off-peak. The workday peak period is from 7:00 to 9:00 and from 17:00 to 20:00, and the off-peak period is the remaining period. There is no obvious peak and off-peak on weekends, so weekends are considered as a whole period.

## 
我们使用WebGIS技术将道路骑行量统计结果在网页中显示，用户在点击感兴趣的道路后可以查看详细信息。
We use WebGIS technology to display the road cycling volume statistics results on the webpage. Users can view detailed information by clicking on the road of interest.

##


[1, 1, 3, 23, 386, 6366, 40314, 92381, 109403, 111531, 112119, 112194, 0]

最终，我们将所有POI转化为GeoHASH code并构建了一颗深度为12的前缀树，左图记录了前九层的节点数目，可以发现越往下节点数目越多。总体而言，这颗前缀树的性能满足我们的需求，能够在较短时间内完成POI的查找。

Finally, we converted all POIs into GeoHASH codes and built a prefix tree with a depth of 12. The left figure records the number of nodes in the first nine layers. It can be found that the number of nodes increases as it goes down. Overall, the performance of this prefix tree meets our requirements and can complete the POI search in a short time.

## Framework Long-Long Time Running Task Management
轨迹的路网匹配任务总共耗费了差不多3天时间，为此我们设计了一个长时间运行任务管理框架，部署在实验室的电脑上。该框架会自动将任务分解为多个可以并行处理的小任务，并将运行结果输出到log文件中。我们还在其中集成了一个邮件机器人（Email Bot），每隔一段时间从log中抓取最新的运行结果并发送到指定的邮箱中。这样，我们可以随时随地查看任务的运行情况，而不必时刻盯着电脑。

The trajectory road network matching task took almost 3 days. For this reason, we designed a long-time running task management framework, which was deployed on the computer in the laboratory. The framework automatically decomposes the task into multiple small tasks that can be processed in parallel and outputs the running results to the log file. We also integrated an email bot in it, which grabs the latest running results from the log and sends them to the specified email every once in a while. In this way, we can check the running status of the task anytime and anywhere without having to stare at the computer all the time.

每5个小时

Every 5 hours