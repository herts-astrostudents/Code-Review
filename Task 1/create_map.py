from __future__ import print_function, division
import numpy as np
from operator import add
import matplotlib.pyplot as plt


def make_gaussian_star(shape, position, flux, width=None):
    """
	Makes a gaussian star 
	shape: shape of the array in which to place the star
	position: indexing position of the array
	flux: amplitude of star
	width: the gaussian width. If None, then the star will be one pixel
	"""
    if width is None:
        a = np.zeros(shape)
        a[position[0], position[1]] = flux
        return a
    ygrid, xgrid = np.mgrid[:shape[0], :shape[1]]
    yy = (position[0] - ygrid) ** 2 / (2 * width)
    xx = (position[1] - xgrid) ** 2 / (2 * width)
    return flux * np.exp(-(xx + yy))


def generate_map(shape, nstars, noise=0, real_stars=False, allow_blended=False, allow_bordered=False, min_snr=3,
                 max_snr=10, max_width=None, seed=0):
    np.random.seed(seed)
    array = np.random.normal(0, noise, shape)
    fluxes = np.random.uniform(min_snr * noise + 0.01, max_snr * noise + 0.01, nstars)
    if max_width is None:
        max_width = int(min(shape) * 0.1)
    if real_stars:
        widths = np.random.uniform(1, max_width, nstars)
        mw = max(widths)
    else:
        widths = [None] * nstars
        mw = 0

    positions = []
    for flux, width in zip(fluxes, widths):
        allowed_position = False
        while not allowed_position:
            position = np.random.uniform([mw, mw], [array.shape[0] - mw, array.shape[1] - mw]).astype(int)
            if not allow_blended:
                dists = [np.linalg.norm(p - position) for p in positions]
                if real_stars:
                    allowed_position = not any([d <= w + width for w, d in zip(widths, dists)])
                else:
                    allowed_position = not any([d <= 0 for d in dists])
            else:
                break
        positions.append(position)
        array += make_gaussian_star(array.shape, position, flux, width)

    positions = np.asarray(positions)
    return array, (positions, fluxes, widths)


def plot_map(array, positions=None, **kwargs):
    plt.imshow(array)
    plt.colorbar()
    plot_positions(positions, **kwargs)


def plot_positions(positions, **kwargs):
    if positions is not None:
        y, x = zip(*positions)
        plt.scatter(x, y, edgecolors=kwargs.pop('edgecolors', 'r'), facecolors=kwargs.pop('facecolors', 'none'),
                    s=kwargs.pop('s', 80), **kwargs)


if __name__ == '__main__':
    def find_stars(array):
        pos = np.asarray(list(zip(*np.where(array > 0))))
        return pos, array[pos]
