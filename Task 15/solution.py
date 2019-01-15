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
    mean, median, std = sigma_clipped_stats(image, sigma=3.0, iters=5)
    daofind = DAOStarFinder(fwhm=3.0, threshold=9.*std)
    sources = daofind(image - median)

    top_flux_indices = sources.argsort(keys="peak")
    sources = sources[top_flux_indices[::-1][0:nstars]]

    edge_distance = 0
    sources = sources[ 
        (sources["xcentroid"] > edge_distance) & \
        (sources["xcentroid"] < image.shape[0] - edge_distance) & \
        (sources["ycentroid"] > edge_distance) & \
        (sources["ycentroid"] < image.shape[1] - edge_distance)
    ]
    
    stamps = [ 
        Cutout2D(image, position=(int(round(s["xcentroid"])), int(round(s["ycentroid"]))), size=size, mode="partial", fill_value=median).data
        for s in sources
        ]

    psf = np.median(stamps, axis=0)
    return psf