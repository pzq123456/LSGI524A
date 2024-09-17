import time
import pandas as pd
import matplotlib.pyplot as plt
# from pyreproj import Reprojector


# transform = Reprojector().get_transformation_function(from_srs=4326, to_srs='epsg:26916')

PARENT_PATH = 'LSGI524A/assiment1'

SAVE_PATH1 = PARENT_PATH + '/data/chicago_data_cleaned.csv'
SAVE_PATH2 = PARENT_PATH + '/data/station_cleaned.csv'

# Trip duration : Max value, Min value, Median, Mean, 25% percentile, 75% percentile, Standard deviation
def getStatistics(column):
    # save the statistics as a dictionary
    statistics = {
        'Max value': column.max(),
        'Min value': column.min(),
        'Median': column.median(),
        'Mean': column.mean(),
        '25% percentile': column.quantile(0.25),
        '75% percentile': column.quantile(0.75),
        'Standard deviation': column.std()
    }

    # print the statistics
    for key, value in statistics.items():
        print(key, ': ', value)
    
    return statistics


def visualizeStatistics(statistics, title="Boxplot with Standard Deviation"):
    fig, ax = plt.subplots()
    
    box_data = [
        [statistics['Min value'], statistics['25% percentile'], statistics['Median'], statistics['75% percentile'], statistics['Max value']]
    ]
    positions = [1]
    widths = 0.5
    ax.boxplot(box_data, positions=positions, widths=widths)
    ax.set_title(title)
    plt.show()


if __name__ == '__main__':
    # load the cleaned data
    # df = pd.read_csv(SAVE_PATH1)
    # # get the statistics of the trip duration
    # trip_duration = df['tripduration']
    # # convert the str to numeric as int ignore the numbers afther the dot
    # trip_duration = pd.to_numeric(trip_duration, errors='coerce').dropna().astype(int)
    # # get the statistics
    # trip_duration_statistics = getStatistics(trip_duration)
    # visualizeStatistics(trip_duration_statistics, title = "Trip Duration Boxplot with Standard Deviation")

    # 计算时间 执行 transform 的时间
    # print(transform(47.46614, 7.80071))

    # runing time for transform
    start = time.time()
    transform(47.46614, 7.80071)
    end = time.time() # runing time for transform:  0.026226043701171875
    print('runing time for transform: ', (end - start) * 1000)
