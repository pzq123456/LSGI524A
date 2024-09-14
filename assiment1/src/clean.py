import pandas as pd
import tqdm

# data path
PARENT_PATH = 'LSGI524A/assiment1'

PATH1 = PARENT_PATH + '/data/chicago_data.csv'
PATH2 = PARENT_PATH + '/data/station.csv'

SAVE_PATH1 = PARENT_PATH + '/data/chicago_data_cleaned.csv'
SAVE_PATH2 = PARENT_PATH + '/data/station_cleaned.csv'

'''
For the chicago_data.csv file,
Drop  columns  that  will  not  be  used  
(i.e., usertype, gender and birthyear); 
Drop records whose start_time and end_time are 
not between 00:00:00 and 23:59:59, 25 July 2019; 
Drop records with any missing values;
'''

# trip_id
# start_time
# end_time
# bikeid
# tripduration
# from_station_id
# from_station_name
# to_station_id
# to_station_name

# usertype
# gender
# birthyear

# columns to add in final data, for another word, extrect the location information 
# from_station_lat
# from_station_lon
# to_station_lat
# to_station_lon

# clean the chicago data
def clean_chicago_data():
    df = pd.read_csv(PATH1)
    # 1. Drop  columns  that  will  not  be  used
    toDrop =  ['usertype','gender','birthyear']
    df = df.drop(toDrop, axis=1)
    # 2. Drop records whose start_time and end_time are not between 00:00:00 and 23:59:59, 25 July 2019
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    df = df[(df['start_time'].dt.time >= pd.to_datetime('00:00:00').time()) & (df['start_time'].dt.time <= pd.to_datetime('23:59:59').time())]
    # 3. Drop records with any missing values
    df = df.dropna()
    # 4. Add location information SUSPENDED
    # save the cleaned data 
    df.to_csv(SAVE_PATH1, index=False)

# data__stations__name
# data__stations__has_kiosk
# data__stations__electric_bike_surcharge_waiver,
# data__stations__region_id,
# data__stations__short_name,
# data__stations__lat,
# data__stations__lon,
# data__stations__capacity,
# data__stations__external_id,
# data__stations__eightd_has_key_dispenser,
# data__stations__station_id,
# data__stations__rental_uris__ios,
# data__stations__rental_uris__android,
# data__stations__rental_methods__001,
# data__stations__rental_methods__002,
# data__stations__rental_methods__003,
# data__stations__station_type,
# last_updated,
# ttl

# clean the station data
def clean_station_data():
    # 只保留以下字段 ['data__stations__station_id', 'data__stations__name', 'data__stations__lat', 'data__stations__lon']
    df = pd.read_csv(PATH2)
    df = df[['data__stations__station_id', 'data__stations__name', 'data__stations__lat', 'data__stations__lon']]
    df.columns = ['id', 'name', 'lat', 'lon']
    df.to_csv(SAVE_PATH2, index=False)

if __name__ == '__main__':
    clean_chicago_data()
    clean_station_data()
    print('cleaned data saved to',SAVE_PATH2)