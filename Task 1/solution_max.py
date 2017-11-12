from create_map import generate_map, plot_map, plot_positions
import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table

import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from mpl_toolkits.mplot3d import Axes3D

def Gauss2D_assymetric((x,y), amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    xo = float(xo)
    yo = float(yo)    
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)

    g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) + c*((y-yo)**2)))

    return g.ravel()

def Gauss2D( (x,y), a, dz, x0, y0, sigx, sigy):
	gx = ((x - x0)**2) / (2.0*(sigx**2))
	gy = ((y - y0)**2) / (2.0*(sigy**2))

	g = dz + a*np.exp( -(gx + gy))
	
	return g.ravel()

def getmax(arr):
	arr = np.array(arr)
	i, j = np.unravel_index(arr.argmax(), arr.shape)
	return i, j


def find_stars(ccd_image, noise=0.001):
	"""
	Given a `ccd_image`, return an astropy table containing columns called x, y, flux
	"""
	y = np.linspace(0, ccd_image.shape[1]-1, ccd_image.shape[1])
	x = np.linspace(0, ccd_image.shape[0]-1, ccd_image.shape[0])
	x,y = np.meshgrid(x, y)

	xs, ys, fs = [],[],[]
	while True:
		imax, jmax = getmax(ccd_image)

		if ccd_image[imax, jmax] < 5*np.std(ccd_image):
			break

		# plt.imshow(ccd_image)
		# plt.show()

		# fit to the whole CCD
		initial_guess = (float(ccd_image[imax, jmax]), 0.0, float(jmax), float(imax), 2.0, 2.0)
		popt, pcov = curve_fit(Gauss2D, (x,y), ccd_image.ravel(), p0=initial_guess)
		ccd_image_fit = Gauss2D((x,y), *popt).reshape(ccd_image.shape[0], ccd_image.shape[1])

		# fit to the area around the star
		# optional
		ccd_image_cut = np.array(list(ccd_image))
		ccd_image_cut[ ccd_image_fit < 0.01*ccd_image_fit[imax, jmax] ] = 0.0
		popt, pcov = curve_fit(Gauss2D, (x,y), ccd_image_cut.ravel(), p0=popt)

		# get fit
		ccd_image_fit = Gauss2D((x,y), *popt).reshape(ccd_image.shape[0], ccd_image.shape[1])

		# add the star to the list
		xs.append(round(popt[2]))
		ys.append(round(popt[3]))
		fs.append(popt[0])

		# substract fitted star
		ccd_image -= ccd_image_fit

	catalogue = Table([xs, ys, fs], names=('x', 'y', 'flux'))

	return catalogue


def verify(star_catalogue, ccd_image, true_positions, true_fluxes):
	positions = [(y, x) for y, x in zip(star_catalogue['y'], star_catalogue['x'])]
	missed = set([(y, x) for y, x in true_positions.tolist()]) - set(positions)
	plt.figure()
	plot_map(ccd_image)
	if len(positions):
		plot_positions(positions, edgecolors='g', label='found')
	if len(missed):
		plot_positions(missed, edgecolors='r', label='missed')
	s = '{:.0f}/{:.0f} missed. {:.0f} fake sources found'.format(len(missed), len(star_catalogue), len(positions)-len(star_catalogue))
	plt.title(s)
	print(s)

	diff_flux = true_fluxes - star_catalogue['flux']
	plt.figure()
	plt.hist(diff_flux, bins=int(len(true_fluxes)/3))
	plt.xlabel(r'$\Delta flux$')
	plt.ylabel('N')
	print("flux deviation from true flux = {}+-{}".format(np.nanmean(diff_flux), np.nanstd(diff_flux)))


def shitty_find_stars(array):
	pos = np.asarray(list(zip(*np.where(array > 0))))
	t = Table(data=pos, names=['y', 'x'])
	t['flux'] = 1
	return t


if __name__ == '__main__':
	shape = (500, 500)
	nstars = 50
	noise = 0.001

	print 'generating map ...',
	image, (positions, fluxes, widths) = generate_map(shape, nstars, noise=noise, real_stars=True, 
												  allow_blended=False, allow_bordered=True, 
												  min_snr=3, max_snr=10)  # change these options!
	print ' done'

	print 'looking for the stars ...',
	catalogue = find_stars(image, noise)
	print ' done'

	print 'verifying stars ...',
	verify(catalogue, image, positions, fluxes)
	print ' done'

	plt.show()