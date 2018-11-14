import numpy as np
import matplotlib.pyplot as plt
import time

# Load ra and dec
X = np.loadtxt('ra_dec.csv')

# Target ra and dec for nearest neighbour search
target_X = np.array([34.3509123, -5.328912])

# Plot positions
fig, ax = plt.subplots(figsize=(10,10))
ax.plot(X[:,0], X[:,1], '.k')
ax.set_ylabel('Dec / degrees')
ax.set_xlabel('RA / degrees')
ax.plot(target_X[0], target_X[1], 'xr', markersize=20)

def nearest_neighbour_linear(X, target_X):
    distance = lambda a, b: np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    closest_index = np.argmin( [distance(x, target_X) for x in X] )
    return closest_index

def nearest_neighbour_ktree(X, target_X):
    from scipy import spatial
    tree = spatial.KDTree(X)
    distance, index = tree.query(np.array(target_X))
    
    return index

def nearest_neighbour(X, target_X):
    """
    Find the index of the nearest point in X to the target position
    """
    return nearest_neighbour_ktree(X, target_X)

start = time.time()
# Find the index of the nearest point
index = nearest_neighbour(X, target_X)
end = time.time()
print('Elapsed time:', end - start)

# Plot the nearest point to the target
ax.plot(X[index, 0], X[index, 1], 'ob')

plt.show()
