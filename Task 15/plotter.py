from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np


def gaussian_fit(x, y, oversample=10):
    '''
    Fit a Gaussian

    x, y: arrays, data to fit Gaussian to
    oversample: int, oversample the fit curve by this factor

    returns fit result - x and y arrays, sigma of the fit
    '''
    gaussian = lambda x, a, x0, sigma, dy: a*np.exp(-(x-x0)**2/(2*sigma**2)) + dy
    popt, pcov = curve_fit(gaussian, x, y, 
        p0=[max(y), 
            x[np.argmax(y)], 
            len(x)/10,
            min(y)])
    
    x_fit = np.linspace(min(x), max(x), oversample*len(x))
    y_fit = gaussian(x_fit, *popt)

    return x_fit, y_fit, popt[2]


def plot_psf(image, psf, colormap="gray"):
    '''
    Plots the image, PSF and X/Y slices of the PSF.
    Does NOT call plt.show()

    image: tuple like (<name str>, <image 2D array>)
    psf: tuple like (<name str>, <psf image 2D array>)
    '''
    f, ax = plt.subplots(2, 2, figsize=(8, 8))
    
    ax[0, 1].imshow(image[1], cmap=colormap)
    ax[0, 1].set_title("{} image".format(image[0]))
    ax[0, 1].set_xlabel("x, px")
    ax[0, 1].set_ylabel("y, px")

    ax[1, 0].imshow(psf[1], cmap=colormap)
    ax[1, 0].set_title("PSF")
    ax[1, 0].set_xlabel("x, px")
    ax[1, 0].set_ylabel("y, px")

    xslice = psf[1][psf[1].shape[0]//2]
    ax[0, 0].step(range(len(xslice)), xslice, where="mid")
    x_fit, y_fit, sigma = gaussian_fit(range(len(xslice)), xslice, oversample=10)
    ax[0, 0].plot(x_fit, y_fit, label="sigma = {0:.2f}px".format(sigma))
    ax[0, 0].legend(loc="upper left")
    ax[0, 0].set_xlabel("x, px")
    ax[0, 0].set_ylabel("flux")

    yslice = psf[1].T[psf[1].shape[1]//2]
    ax[1, 1].step(yslice, range(len(yslice)), where="mid")
    x_fit, y_fit, sigma = gaussian_fit(range(len(yslice)), yslice, oversample=10)
    ax[1, 1].plot(y_fit, x_fit, label="sigma = {0:.2f}px".format(sigma))
    ax[1, 1].legend(loc="lower right")
    ax[1, 1].set_xlabel("flux")
    ax[1, 1].set_ylabel("y, px")
    ax[1, 1].invert_yaxis()

    plt.tight_layout()