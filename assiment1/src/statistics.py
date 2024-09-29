import pandas as pd
import matplotlib.pyplot as plt

PARENT_PATH = 'assiment1'

SAVE_PATH1 = PARENT_PATH + '/data/chicago_data_cleaned.csv'
SAVE_PATH4 = PARENT_PATH + '/data/output.csv'

# Trip duration : Max value, Min value, Median, Mean, 25% percentile, 75% percentile, Standard deviation
def getStatistics(column, title="Statistics"):
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

    print(title)
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

def task2():
    # load the cleaned data
    df = pd.read_csv(SAVE_PATH1)
    # get the statistics of the trip duration
    trip_duration = df['tripduration']
    # convert the str to numeric as int ignore the numbers afther the dot
    trip_duration = pd.to_numeric(trip_duration, errors='coerce').dropna().astype(int)
    # get the statistics
    trip_duration_statistics = getStatistics(trip_duration, title="Trip Duration Statistics")
    # if you want to visualize the statistics
    # visualizeStatistics(trip_duration_statistics, title = "Trip Duration Boxplot with Standard Deviation")

    # load the cleaned data
    df = pd.read_csv(SAVE_PATH4)
    # get the statistics of the trip duration
    trip_distances = df['distance']
    # save 2 decimal points
    trip_distances = pd.to_numeric(trip_distances, errors='coerce').dropna().round(2)
    # 剔除异常值 0.0
    trip_distances = trip_distances[trip_distances != 0.0]
    # get the statistics
    trip_distances_statistics = getStatistics(trip_distances, title="Trip Distance Statistics")
    # if you want to visualize the statistics
    # visualizeStatistics(trip_distances_statistics, title = "Trip Distance Boxplot with Standard Deviation")

if __name__ == '__main__':
    task2()
