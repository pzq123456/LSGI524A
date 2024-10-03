from sklearn.cluster import DBSCAN
import dask.dataframe as dd
from tqdm import tqdm
from dask.diagnostics import ProgressBar

PARENT_PATH = 'assiment1' # linux path
SAVE_PATH5 = PARENT_PATH + '/data/ststion_transformed.csv'

SAVE_PATH6 = PARENT_PATH + '/data/clustered_bike_stations_with_clusters.csv'
SAVE_PATH7 = PARENT_PATH + '/data/clustered_bike_stations.csv'


def cluster_stations():
    # Step 1: Load the dataset using Dask
    print("Loading dataset...")
    with ProgressBar():
        data = dd.read_csv(SAVE_PATH5)
        stations = data[['id', 'x_transformed', 'y_transformed']].compute()
    
    # Step 2: Apply DBSCAN with a progress message
    print("Clustering stations...")
    db = DBSCAN(eps=600, min_samples=2)
    
    # Wrap DBSCAN with tqdm progress bar
    stations['cluster'] = tqdm(db.fit_predict(stations[['x_transformed', 'y_transformed']]), 
                               desc="Running DBSCAN")

    # Step 3: Merge cluster labels back to the original data
    print("Merging results...")
    with ProgressBar():
        data = data.merge(stations[['id', 'cluster']], on='id', how='left')

    # Step 4: Compute the final result with progress
    print("Computing final results...")
    with ProgressBar():
        result = data.compute()

    # Step 5: Filter clusters and group stations
    print("Filtering clusters...")
    clusters = result[result['cluster'] != -1]

    print("Grouping station IDs by clusters...")
    clustered_stations = clusters.groupby('cluster')['id'].apply(list).reset_index()

    # Step 6: Get number of clusters and output results
    num_clusters = clustered_stations.shape[0]
    print(f"Number of clusters: {num_clusters}")
    print("Station IDs in each cluster:")
    print(clustered_stations)

    # Step 7: Save the results to CSV files
    print("Saving results to CSV...")
    result.to_csv(SAVE_PATH6, index=False)
    clustered_stations.to_csv(SAVE_PATH7, index=False)

    print("Clustering completed.")


if __name__ == '__main__':
    cluster_stations()