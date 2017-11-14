from create_map import generate_map, plot_map, plot_positions
import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table, vstack
from scipy.optimize import leastsq
from functools import reduce
from itertools import product
from operator import or_


def overlap_sets(sets):
	"""
	sets: a list of sets
	returns a set of sets which do not overlap made by joining any overlapping set that is given
	"""
	supersets = []
	while sets:
		s = sets[0]
		other_sets = sets[1:]
		supersets.append(s)
		del sets[0]
		for i, other in enumerate(other_sets):
			if other & supersets[-1]:
				supersets[-1] |= other
				del sets[i]
	return supersets


def estimate_background(array):
	return np.nanmedian(array), np.nanstd(array)


def sigma_clip(array, sigma, maxiter=10, frac_tol=0.01):
	old_median = np.nan
	mask = slice(None)
	for i in range(maxiter):
		new_median, new_std = estimate_background(array[mask])
		mask = array <= new_median + (new_std *sigma)
		diff = new_median - old_median
		if diff <= frac_tol * old_median:
			break
		old_median = new_median
	return ~mask, new_median, new_std


def gaussian_2d(yy, xx, y0, x0, width, peak):
	x = (xx - x0)**2 / 2 / width / width
	y = (yy - y0)**2 / 2 / width / width
	return np.exp(-x - y) * peak


def get_gaussians(n):
	"""
	returns function that accepts x/y centres, widths and peaks in order
	"""
	def func(params, y, x):
		return sum(gaussian_2d(y, x, *params[i:i+4]) for i in range(0, n*4, 4))
	return func


def fit_gaussians(array, centre_guesses, mask, label_mask):
	"""
	Fits gaussians to masked array where masked area is not to be included in the fit
	Returns centres, widths and peak
	"""
	N = len(centre_guesses)
	this_label_mask = label_mask[mask]
	labels = set(this_label_mask.astype(int).ravel().tolist())
	integrated_flux_guesses = np.asarray([array[mask][this_label_mask == l].sum() for l in labels])
	peak_flux_guesses = integrated_flux_guesses / np.sqrt(np.pi)
	std_guesses = np.asarray([np.sqrt((this_label_mask == l).sum() / np.pi) for l in labels])
	
	gaussians = get_gaussians(n=N)
	yy, xx = np.mgrid[:array.shape[0], :array.shape[1]]
	leastsq_gaussian = lambda p: gaussians(p, yy, xx)[mask] - array[mask]
	p0 = np.concatenate([centre_guesses, std_guesses[:, None], peak_flux_guesses[:, None]], axis=1)  # nx4
	p = leastsq(leastsq_gaussian, p0.ravel())[0].reshape(N, 4)
	return p[:, :2], p[:, 2], p[:, 3]


def label_mask(array, mask):
	y_grid, x_grid = np.mgrid[:array.shape[0], :array.shape[1]]
	sort_index = np.argsort(array[mask].ravel())[::-1]  # max to min index of sorted array
	y_coords = y_grid[mask].ravel()[sort_index]
	x_coords = x_grid[mask].ravel()[sort_index]
	values = array[mask].ravel()[sort_index]
	label_mask = np.zeros_like(array)  # 0 == not labelled
	previous_x, previous_y = np.nan, np.nan

	r22 = np.sqrt(2) * 2

	label = 1
	for y, x, val in zip(y_coords, x_coords, values):
		adjacent_label = label_mask[max([0,y-1]):min([y+2, array.shape[1]]), max([0, x-1]):min([x+2, array.shape[1]])].max()
		if adjacent_label > 0:
			label_mask[y, x] = adjacent_label
		else:
			label_mask[y, x] = label
			label += 1
		previous_y, previous_x = y, x
	filters = [label_mask == label for label in range(1, int(label_mask.max()+1))]
	centroid = [((y_grid[f] * array[f]).sum() / array[f].sum(), (x_grid[f] * array[f]).sum() / array[f].sum()) for f in filters]
	return np.asarray(centroid), label_mask


def segment_image(image, mask, lim_npix=4):
	centroids, segmentation = label_mask(image, mask)
	
	# roll 
	n = 0
	stacked = np.zeros((9,) + segmentation.shape)
	directions = [0, 1, -1]
	for i in directions:  # ['up', 'down', '']
		for j in directions:  #['left', 'right', '']:
			stacked[n, 1:-1, 1:-1] = np.roll(np.roll(segmentation, i, axis=0), j, axis=1)[1:-1, 1:-1]  # exclude sides
			n += 1
			
	allowed_labels = []
	for i, label in enumerate(range(1, len(centroids)+1)):
		filt = segmentation == label
		if filt.sum() < lim_npix:
			segmentation[filt] = np.sort(np.where(stacked != label, stacked, 0)[:, filt])[-1]
		else:
			allowed_labels.append(label)

	groups = [set(stacked[:, segmentation == label].ravel().tolist()) for label in allowed_labels]
	groups = {frozenset(g - {0}) for g in groups}  # remove background group and duplicates
	groups = overlap_sets(list(groups))

	segments = []
	for group in groups:
		if len(group):
			group_mask = reduce(or_, [segmentation == label for label in group])
			centre_guesses = centroids[[int(i-1) for i in group]]
			segments.append((centre_guesses, group_mask))
	return segments, segmentation


def fit_gaussian_to_segments(image, segments, segmentation_mask):
	ts = []
	for centre_guesses, group_mask in segments:
		positions, widths, fluxes = fit_gaussians(image, centre_guesses, group_mask, segmentation_mask)
		ts.append(Table([positions[:, 0], positions[:, 1], fluxes, widths], names=['y', 'x', 'flux', 'width']))
	return vstack(ts)
		

def model_map(ccd_image, catalogue):
	yy, xx = np.mgrid[:ccd_image.shape[0], :ccd_image.shape[1]]
	model = np.zeros_like(ccd_image)
	for row in catalogue:
		model += gaussian_2d(yy, xx, row['y'], row['x'], row['width'], row['flux'])
	return model, ccd_image - model
	

def find_stars(ccd_image, sigma):
	mask, background, background_err = sigma_clip(ccd_image, sigma)
	segments, label_mask = segment_image(image-background, mask)
	return fit_gaussian_to_segments(image, segments, label_mask)


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


if __name__ == '__main__':
	image, data = generate_map((20, 20), 5, noise=0., real_stars=True, allow_blended=True, allow_bordered=True, seed=10)
	# plot_map(image, data[0])
	# plt.figure()	
	table = find_stars(image, 2)
	# model, residual = model_map(image, table)
	plot_map(image, table[['y', 'x']])
	# # plot_positions(, edgecolor='y')
	# print(table)
	# print(data)
	plt.show()