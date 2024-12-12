# URBAN AND GEOSPATIAL BIG DATA ANALYTICS (LSGI 524A) 
## Spatiotemporal Analysis of Bike-sharing Patterns and Influencing Factors at the Street Scale: **A Case Study of Shanghai**

> - by Group 4 LSGI PolyU
> - Jianwen Zeng, Zhiqing Pan, Guohao Zou 
> - 2024/25 Semester 1 LSGI524A Project

## Abstract
### [Objective] 
As an Internet-based mobility service, shared bicycles have become the preferred mode of short-distance travel due to their unique business model, low cost and environmental friendliness. By analyzing the large volume of trajectory data accumulated through the background service of  shared bicycles and integrating it with a suitable data processing and analysis framework, the travel patterns of shared bicycles can be effectively explored. However, most studies are limited to origin-destination (OD) analysis and fail to reveal the factors influencing shared bicycle travel at the road scale. 

### [Methods] 
This study takes Shanghai as an example: Using the GPS trajectory data of shared bicycles and multi-source big data, 97,967 cycling trajectories were reconstructed using GeoHash encoding, the nearest neighbor matching algorithm, and the hidden markov model. Through the big data analysis methods, we aggregate the cycling volume on roads at different time periods, map the cycling duration and distance, and extract peak and off-peak periods. Additionally, combined with points of interest (POI) data, a greedy algorithm is used to identify the travel destinations of shared bicycles. The DeeplabV3+ deep learning model is employed for semantic segmentation of 54,940 street view images, extracting the proportion of 19 street view elements. A random forest model (RF) was utilized with 16 independent variables, including street view elements, for regression modeling. Factor importance analysis and partial dependence plots were used to reveal the impact of each factor on road cycling volumes. 

### [Results]
The results indicate that the bike-sharing usage exhibits distinct temporal patterns, with weekday peaks occurring during morning and evening commuting hours, while weekend peaks are concentrated in the afternoon. Shared bikes primarily serve as short-distance travel tools, with rides under 2 km and less than 1 minute being dominant. And often used for cycling to destinations such as shopping malls, transportation hubs, and catering services. Hotspots of cycling activity are concentrated in Shanghai's central districts, particularly Huangpu, Jing'an, Hongkou, and Yangpu districts. Using 16 explanatory variables, the random forest models effectively predicted street-level cycling volumes. Key influencing factors include residential density, road classification, and distance to metro stations. Nonlinear relationships were observed, with higher cycling volumes in regions with greater cycling volumes, and cycling volume is higher when the distance to metro stations is less than 2.5 km. 

### [Significance] 
This study provides scientific support for sustainable urban planning and the scientific management of shared bicycles, contributing to the promotion of low-carbon shared mobility in Shanghai.

## Keywords: 
Shared bicycle; spatiotemporal patterns; trajectory reconstruction; random forest model; street scale

## Repository Structure
```
/Project
    /Data
    /src
    /webpages
    /README.md
    /Group No.4_Manuscript.pdf
```
Where the `Data` folder contains the data required for this project, the `src` folder contains the `Python` code for this project, the `webpages` folder contains the web files for this project, and the `Group No.4_Manuscript.pdf` file is the final draft of the paper for this project.
