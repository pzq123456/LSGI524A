import pandas as pd
import tqdm

# data path
# PARENT_PATH = '/LSGI524A/assiment1' # linux path
PARENT_PATH = 'G:/polyulessons/LSGI524A/assiment1' # windows path

PATH1 = PARENT_PATH + '/data/chicago_data.csv'
PATH2 = PARENT_PATH + '/data/station.csv'

SAVE_PATH1 = PARENT_PATH + '/data/chicago_data_cleaned.csv'
SAVE_PATH2 = PARENT_PATH + '/data/station_cleaned.csv'
SAVE_PATH3 = PARENT_PATH + '/data/locations.csv' 


# clean the chicago data
def clean_chicago_data():
    df = pd.read_csv(PATH1)
    # 1. Drop  columns  that  will  not  be  used
    toDrop =  ['usertype','gender','birthyear']
    df = df.drop(toDrop, axis=1)
    # 2. Drop records whose start_time and end_time are not between 00:00:00 and 23:59:59, 25 July 2019
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    # pick up between 00:00:00 and 23:59:59 on 25 July 2019
    df = df[(df['start_time'] >= pd.to_datetime('2019-07-25 00:00:00')) & 
            (df['start_time'] <= pd.to_datetime('2019-07-25 23:59:59'))]

    df = df[(df['end_time'] >= pd.to_datetime('2019-07-25 00:00:00')) & 
            (df['end_time'] <= pd.to_datetime('2019-07-25 23:59:59'))]


    # 3. Drop records with any missing values
    df = df.dropna()
    # 指定 id 类型为 int
    df['trip_id'] = df['trip_id'].astype(int)
    df['bikeid'] = df['bikeid'].astype(int)
    df['from_station_id'] = df['from_station_id'].astype(int)
    df['to_station_id'] = df['to_station_id'].astype(int)
    # save the cleaned data 
    df.to_csv(SAVE_PATH1, index=False)

# clean the station data
def clean_station_data():
    df = pd.read_csv(PATH2)
    df = df[['data__stations__station_id', 'data__stations__name', 'data__stations__lat', 'data__stations__lon']]
    df.columns = ['id', 'name', 'lat', 'lon']
    df.to_csv(SAVE_PATH2, index=False)

# Drop records whose station ids are not in station.csv. 
def drop_invalid_station():
    df1 = pd.read_csv(SAVE_PATH1)
    df2 = pd.read_csv(SAVE_PATH2)
    valid_station_id = set(df2['id'])
    df1 = df1[(df1['from_station_id'].isin(valid_station_id)) & (df1['to_station_id'].isin(valid_station_id))]
    df1.to_csv(SAVE_PATH1, index=False)

# load the cleaned data and get the answer
def get_answer_task1():
    df = pd.read_csv(SAVE_PATH1)
    # 1) How many valid bicycle trips were documented on 25 July 2019? 
    print('1) How many valid bicycle trips were documented on 25 July 2019? ', len(df))
    # 2) How many bike stations were used on that day? (unique station both in from and to)
    print('2) How many bike stations were used on that day? ', len(set(df['from_station_id'].unique()) | set(df['to_station_id'].unique())))
    # 3) How many unique bikes were used?
    print('3) How many unique bikes were used? ', len(df['bikeid'].unique()))

# main function

def getLocations():
    print('get O-D locations(Lon,Lat) for each trip...')
    # chicago_data_cleaned 中记录的 from_station_id 和 to_station_id
    # 从 station_cleaned 中找到对应的经纬度 并按照顺序存储到 locations.csv
    # columns : trip_id, from_station_id, to_station_id, from_lat, from_lon, to_lat, to_lon
    df1 = pd.read_csv(SAVE_PATH1)
    df2 = pd.read_csv(SAVE_PATH2)
    df2 = df2.set_index('id')
    locations = []
    # for index, row in df1.iterrows():
    for index, row in tqdm.tqdm(df1.iterrows(), total=df1.shape[0]):
        from_id = row['from_station_id']
        to_id = row['to_station_id']
        from_lat = df2.loc[from_id]['lat']
        from_lon = df2.loc[from_id]['lon']
        to_lat = df2.loc[to_id]['lat']
        to_lon = df2.loc[to_id]['lon']
        locations.append([row['trip_id'], from_id, to_id, from_lat, from_lon, to_lat, to_lon])
    
    locations = pd.DataFrame(locations, columns=['trip_id', 'from_station_id', 'to_station_id', 'from_lat', 'from_lon', 'to_lat', 'to_lon'])
    # 指定 id 类型为 int
    locations['trip_id'] = locations['trip_id'].astype(int)
    locations['from_station_id'] = locations['from_station_id'].astype(int)
    locations['to_station_id'] = locations['to_station_id'].astype(int)
    locations.to_csv(SAVE_PATH3, index=False)
    print('locations saved to', SAVE_PATH3)

def task1():
    '''
    **Usage**:
        - run the ```task1()``` function or the following code in the terminal
        - ``` python clean.py ```
        - the cleaned data will be saved to the data folder, and the answer will be printed.
    **Note**:
    need the directory structure as follows:
            /assiment1
                /data
                    chicago_data.csv
                    station.csv
                /src
                    clean.py
    '''

    clean_chicago_data()
    clean_station_data()
    drop_invalid_station()
    print('cleaned data saved to', SAVE_PATH1, 'and', SAVE_PATH2)
    get_answer_task1()

if __name__ == '__main__':
    task1()
    # attach the locations to the cleaned data not for the task1
    # getLocations()