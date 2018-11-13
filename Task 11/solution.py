import numpy as np

def k_means(n_groups, X_data):
    '''
    Use Lloyd's algorithm to separate the data into k = n_groups clusters
    
    n_groups: int: number of clusters
    X_data: np.array: data points, shape = (n_points, n_dimensions)
    returns:
        group_centroids: np.array: mean of each cluster, shape = (n_groups, n_dimensions)
        groups: np.array: group assignment for each data point, shape = (n_points,)
    '''

    return group_centroids, groups
