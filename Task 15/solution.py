from astropy.stats import sigma_clipped_stats
from astropy.nddata import Cutout2D
from photutils import DAOStarFinder
import numpy as np


def estimate_psf(image, nstars=10, size=20):
    '''
    Estimate an empirical psf from the image

    image: 2D array, image with some stars
    nstars: int, number of brightest stars to stack
    size: int, size of the resulting PSF image (square stamp)

    returns a 2D array with the PSF image
    '''
    # do stuff here
    return psf
