import numpy as np
import matplotlib.pyplot as plt
import time
import random

# Load ra and dec
X = np.loadtxt('ra_dec.csv')

# Target ra and dec for nearest neighbour search
target_X = np.array([34.3509123, -5.328912])
# target_X = np.array([3.4358269e+01, -5.4666713e+00])

# Plot positions
fig, ax = plt.subplots(figsize=(6,6))
ax.plot(X[:,0], X[:,1], '.k')
ax.set_ylabel('Dec / degrees')
ax.set_xlabel('RA / degrees')
ax.plot(target_X[0], target_X[1], 'xr', markersize=20)

def nearest_neighbour(X, target_X):
    """
    Find the index of the nearest point in X to the target position
    """

    #################################################

    # 'Solution 1 - search every data point until closest distance found'

    diffs = []

    for i in range(0, len(X)):
    	x_diff = abs(X[i,0] - target_X[0])
    	y_diff = abs(X[i,1] - target_X[1])
    	diff = np.sqrt(x_diff**2 + y_diff**2)
    	diffs.append(diff)

    closest_index = diffs.index(min(diffs))

	#################################################

    # 'Solution 2'

    # separation = 0.1
    # N_points = len(X)
    # closest_index = random.randint(0, N_points)

    # for i in range(0, 10):
    #     print "Iteration {}".format(i)
    #     x_diff = abs(X[rand_index,0] - target_X[0])
    #     y_diff = abs(X[rand_index,1] - target_X[1])
    #     diff = np.sqrt(x_diff**2 + y_diff**2)
    #     if diff < separation:
    #         separation = 0.5 * separation
    #         closest_index
    #     else:
    #         closest_index = random.randint(0, N_points)


    #################################################

    return closest_index

start = time.time()
# Find the index of the nearest point
index = nearest_neighbour(X, target_X)
end = time.time()
print('Elapsed time:', end - start)

# Plot the nearest point to the target
ax.plot(X[index, 0], X[index, 1], 'ob')

plt.show()
