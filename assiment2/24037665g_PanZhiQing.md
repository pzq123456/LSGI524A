# LSGI524A Assignment 2 : Preprocessing and Exploratory Data Analysis of Large-Scale Taxi GPS Traces
> - PanZhiQing 24037665g 
> - repo : https://github.com/pzq123456/LSGI524A/tree/main/assiment2

## (1) How many unique taxis are there in this dataset, and how many trips are recorded?
- Before cleaning the data:
    ``` 
    Number of unique taxis: 13200
    Number of trips recorded: 33983783
    ```
taxi_id, pick_up_time, drop_off_time, pick_up_intersection, drop_off_intersection
其中时间都是unixtime格式，对于时间的要求是
1.时间应该可以被解析出来，即符合unix格式，否则视为无效行删除之
2.pick_up_time应当晚于drop_off_time,否则删除之
对于intersection的要求是：
1. 应当存在于intersection.csv中，否则视为无效删除之
2.起点与终点应当不同，否则视为无效
## (2) What is the distribution of the number of trips per taxi? Who are the top performers?

## (3) How does the daily trip count (i.e., number of trips per day) change throughout the year? Any rhythm or seasonality?

## (4) What is the distribution of the number of departure trips at different locations (i.e., intersections)? What about the distribution of arrival trips? What will you conclude from these two distributions?

## (5) How does the number of trips change over time in a day? (You will be given three dates randomly selected from the dataset, and then plot the hourly variation of trips from the perspective of local time).

## (6) What is the probability distribution of the trip distance (measured as straight-line distance)? How about travel time (i.e., trip duration)? What will you conclude from these two distributions?

## References