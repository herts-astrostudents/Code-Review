from create_map import generate_map, plot_map, plot_positions
import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table


def find_stars(ccd_image):
    """
	Given a `ccd_image`, return an astropy table containing columns called x, y, flux
	"""

    # Your code here


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
    s = '{:.0f}/{:.0f} missed. {:.0f} fake sources found'.format(len(missed), len(star_catalogue),
                                                                 len(positions) - len(star_catalogue))
    plt.title(s)
    print(s)

    diff_flux = true_fluxes - star_catalogue['flux']
    plt.figure()
    plt.hist(diff_flux, bins=int(len(true_fluxes) / 3))
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
    image, (positions, fluxes, widths) = generate_map(shape, nstars, noise=0, real_stars=False,
                                                      allow_blended=False, allow_bordered=False,
                                                      min_snr=3, max_snr=10)  # change these options!
    catalogue = find_stars(image)
    verify(catalogue, image, positions, fluxes)

    plt.show()