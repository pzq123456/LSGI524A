# LSGI524A Assignment 2 : Preprocessing and Exploratory Data Analysis of Large-Scale Taxi GPS Traces
> - PanZhiQing 24037665g 
> - repo : https://github.com/pzq123456/LSGI524A/tree/main/assiment2

## 1.Introduction
In this assignment, you will be dealing with a large-scale taxi GPS dataset. The dataset records millions of taxi trips in Manhattan, New York in a given year. This dataset has been used extensively to study the dynamics of the urban taxi flow. For example, it has been used by a group of researchers at MIT to evaluate the ride sharing potential of the city (Santi et al., 2014) or to estimate the minimum taxi fleet that is able to serve all the travel demand in the city (Vazifeh et al., 2018).

In this assignment, you will be asked to preprocess the dataset, play with it, and derive meaningful statistics through exploratory data analysis. To start, you are provided with the following two files:
    - taxi_id.csv.bz2
    - intersections.csv

The first compressed file (taxi_id.csv.bz2) records the origin and destination of the taxi trips along with the timestamps. For simplicity, the origin and destination of the actual trips have been matched to the nearest road intersections. The format of this file is as follows: 
```
taxi_id, pick_up_time, drop_off_time, pick_up_intersection, drop_off_intersection
```

The taxi_id is a numerical value that uniquely identifies each taxi. pick_up_time and drop_off_time are expressed in Unix epoch time, and pick_up_intersection, drop_off_intersection are the indices of the intersections (numbers from 1 to 4091).

The second file (intersection.csv) represents the street intersections to which pick-up and drop-off points were snapped to. The format of the file is:
```
id, latitude, longitude
```

where id is a progressive identifier from 1 to 4091 and latitude and longitude are the GPS coordinates of the intersection. Below are two screenshots of these road intersections:

## 2. Tasks
> For question (2) – (6), you are required to provide figures along with your answers. Note that some of the above questions are open ended, and the answers could vary among students.

In this section, you will be asked to analyze the dataset - using any software or programming language that you prefer - and then provide answers to the following research questions:

### (1) How many unique taxis are there in this dataset, and how many trips are recorded?
-
### (2) What is the distribution of the number of trips per taxi? Who are the top performers?
-
### (3) How does the daily trip count (i.e., number of trips per day) change throughout the year? Any rhythm or seasonality?
-
### (4) What is the distribution of the number of departure trips at different locations (i.e., intersections)? What about the distribution of arrival trips? What will you conclude from these two distributions?
-
### (5) How does the number of trips change over time in a day? (You will be given three dates randomly selected from the dataset, and then plot the hourly variation of trips from the perspective of local time).
-
### (6) What is the probability distribution of the trip distance (measured as straight-line distance)? How about travel time (i.e., trip duration)? What will you conclude from these two distributions?
-
## 3. What to submit
- A Word document or PDF file with answers to (1) – (6)
- The computer code used in this assignment. If a particular software is used, please elaborate the procedures on how it helps derive the answers.
- The submission due date is **15th November 2024, 11:59 PM**.