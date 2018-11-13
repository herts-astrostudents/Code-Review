import numpy as np
import matplotlib.pyplot as plt
import time
from scipy import spatial

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


def nearest_neighbour(X, target_X):
    """
    Find the index of the nearest point in X to the target position
    """
    # ------------------------
    # Scipy KD tree solution:
    # ------------------------
    # data = spatial.KDTree(X)
    # closest_index = data.query(target_X)[1]

    # ------------------------
    # Linear solution:
    # ------------------------

    min_dist = 99999
    for i in range(len(X)):
    	dist = np.sqrt((target_X[0] - X[i,0])**2 + (target_X[1]-X[i,1])**2)
    	if dist < min_dist:
    		closest_index = i
    		min_dist = dist

    return closest_index

start = time.time()
# Find the index of the nearest point
index = nearest_neighbour(X, target_X)
end = time.time()
print('Elapsed time:', end - start)

# Plot the nearest point to the target
ax.plot(X[index, 0], X[index, 1], 'ob')

plt.show()
