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
    # Initialise by picking a k random data points to be the initial centroids (where k = n_groups)
    pick = np.random.choice(np.arange(0, len(X_data)), size=n_groups, replace=False)
    group_centroids = X_data[pick]

    # Implement group assignment & centroid steps, looping until the group assignments no longer change
    groups = np.zeros(len(X_data))+np.inf
    groups_old = np.zeros(len(X_data))-np.inf
    while not (np.array_equal(groups, groups_old)):
        groups_old = groups.copy()
        # 1. Compute euclidian distance from each centroid
        r = np.vstack([ np.sqrt(np.sum((X_data - cent)**2, axis=1)) for cent in group_centroids ])
        # And assign to a group using minimum distance
        groups = np.argmin(r, axis=0)
        # 2. Compute new centroids and repeat
        group_centroids = np.array([ np.mean(X_data[groups == group], axis=0) for group in range(n_groups)])

    return group_centroids, groups