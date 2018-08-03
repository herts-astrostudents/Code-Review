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
    n_points, n_dimensions = X_data.shape
    assert n_groups <= n_points, "Cannot create more clusters than there are points"
    group_centroids = X_data[np.random.choice(n_points, n_groups)]  # initialise centroids
    finished = False

    while not finished:
        distances_to_centroids = np.sqrt(np.sum((group_centroids[:, None, :] - X_data[None, ...])**2, axis=-1))
        groups = np.argmin(distances_to_centroids, axis=0)
        previous_group_centroids = group_centroids
        group_centroids = np.asarray([np.mean(X_data[groups == i], axis=0) for i in range(n_groups)])
        finished = np.allclose(previous_group_centroids, group_centroids)

    return group_centroids, groups
