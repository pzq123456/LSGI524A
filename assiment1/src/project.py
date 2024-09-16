import dask.dataframe as dd
from pyproj import Transformer
from dask.diagnostics import ProgressBar

transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

PARENT_PATH = 'LSGI524A/assiment1'

SAVE_PATH3 = PARENT_PATH + '/data/data.csv'
SAVE_PATH4 = PARENT_PATH + '/data/output.csv'

def getProjectedDistance():
    # load the data
    df = dd.read_csv(SAVE_PATH3)
    # transform the coordinates
    df['from_x_transformed'], df['from_y_transformed'] = transformer.transform(df['from_lon'], df['from_lat'])
    df['to_x_transformed'], df['to_y_transformed'] = transformer.transform(df['to_lon'], df['to_lat'])
    # calculate the distance
    df['distance'] = ((df['to_x_transformed'] - df['from_x_transformed']) ** 2 + 
                      (df['to_y_transformed'] - df['from_y_transformed']) ** 2) ** 0.5
    
    with ProgressBar():
        # save the data
        df.to_csv(SAVE_PATH4, index=False, single_file=True)

if __name__ == '__main__':
    getProjectedDistance()
