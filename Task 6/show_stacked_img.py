import matplotlib.pyplot as plt
import numpy as np
from solution import median_stacker
from astropy.io import fits

###########################################
#### Change coordinates as necessary
# coords = np.genfromtxt('pixel_coords.txt')
coords = np.genfromtxt('sky_coords.txt')


stacked_img, coords = median_stacker(coords, 'img_field.fits')

img = fits.open('img_field.fits')[0].data


plt.figure(1)
plt.imshow(img, cmap = 'viridis')
plt.scatter(coords[:,0], coords[:,1], marker = 'x', c = 'k')

plt.figure(2)
plt.imshow(stacked_img)
plt.show()