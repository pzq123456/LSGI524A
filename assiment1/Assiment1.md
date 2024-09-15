# Report for Assiment 1 
> - PanZhiQing 24037665g 
> - 2024.9.14 --> 
> - repo : https://github.com/pzq123456/LSGI524A
## Task1 [25 points]:  
### (1) How many valid bicycle trips were documented on 25 July 2019? 
20187
### (2) How many bike stations were used on that day? 
535
### (3) How many unique bikes were used? 
3822

## Task2 [25 points]: 

|Indicator         |  Trip duration(s)  | Trip distance |
| ---              |      ---        |      ---      | 
|Max value         |31243                 |               |
|Min value         |61                 |               |
|Median            |799.0                 |               |
|Mean              |1187.6403626096003                 |               |
|25% percentile    |465.0                 |               |
|75% percentile    |1403.0                 |               |
|Standard deviation|1400.9766896637864                 |               |

## Task3 [25 points]:  
Data visualization based on the processed bike-sharing data. Please use the skills you have gained in data  visualization  to  present  answers  to  the  following  questions.  Both  figures  and  corresponding descriptions should be included in your report. 

### (1) How does the number of departure trips change over 24 hours? Is there any rhythm or pattern?  

### (2) What is the distribution of the number of departure trips at different stations? What about the distribution of arrival trips?  

### (3) What is the distribution of the trip distance (measured as straight-line Euclidean distance)? What will you conclude from this distribution? 

### (4) What is the distribution of the travel time (i.e., trip duration)?

## Task4 [25 points]:  
Suppose the bike-sharing operator plans to manage efficiently by dividing bike stations into multiple service zones based on the distance between stations. Some clustering algorithms (e.g., DBSCAN, SVM) could be useful for the operator.  

Please  refer  to  this  website  to  cluster  all  bike  stations  in  Chicago  using  the  Density-based  Spatial Clustering of Applications with Noise (DBSCAN) algorithm packaged in scikit-learn. The maximum distance between two stations is 600 meters, and the number of samples in a neighborhood for a point 
to be considered as a core point is 2 stations. The other parameters are set as default. Please list the number of clusters and the station ids in each cluster in your report.  
 
 
## Bonus for Task4 [+10 points]:  
Please visualize the clusters using matplotlib or any Python packages you prefer. Here is a reference about how to visualize clusters. If you complete this Bonus part, please embed the figure into your report.  