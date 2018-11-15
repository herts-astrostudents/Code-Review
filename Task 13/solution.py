import numpy as np
import matplotlib.pyplot as plt
import time
from astropy.coordinates import SkyCoord 
from astropy import units as u

# Load ra and dec
X = np.loadtxt('ra_dec.csv')

# Target ra and dec for nearest neighour search
target_X = np.array([34.3509123, -5.328912])

# Plot positions
fig, ax = plt.subplots(figsize=(10,10))
ax.plot(X[:,0], X[:,1], '.k')
ax.set_ylabel('Dec / degrees')
ax.set_xlabel('RA / degrees')
ax.plot(target_X[0], target_X[1], 'xr', markersize=20)


def nearest_neighbour(X, target_X):
        c = SkyCoord(ra=target_X[0]*u.degree,dec =target_X[1]*u.degree)
        catalog = SkyCoord(ra=X[:,0]*u.degree, dec=X[:,1]*u.degree)
        closest_index, d2d, d3d = c.match_to_catalog_sky(catalog)
        return closest_index

start = time.time()
# Find the index of the nearest point
index = nearest_neighbour(X, target_X)
end = time.time()
print('Elapsed time:', end - start)

# Plot the nearest point to the target
ax.plot(X[index, 0], X[index, 1], 'ob')

plt.show()
