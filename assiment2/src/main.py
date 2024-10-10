import os
from utils import unzipbz2
from clean import q1

PARENT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data') # path to data directory
PATH1 = os.path.join(PARENT_PATH, 'taxi_id.csv.bz2') # path to the zipped file
PATH2 = os.path.join(PARENT_PATH, 'intersections.csv') # path to the zipped file

SAVE_PATH1 = os.path.join(PARENT_PATH, 'taxi_id.csv') # path to the unzipped file

if __name__ == '__main__':
    # Task 0
    # Unzip the file and save it in taxi_id.csv
    # unzipbz2(PATH1, SAVE_PATH1)
    # Question 1
    q1()