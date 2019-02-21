from astropy.stats import sigma_clipped_stats
from astropy.nddata import Cutout2D
from photutils import DAOStarFinder
import numpy as np
import matplotlib.pyplot as plt 


def estimate_psf(image, nstars=50, size=25):
    '''
    Estimate an empirical psf from the image

    image: 2D array, image with some stars
    nstars: int, number of brightest stars to stack
    size: int, size of the resulting PSF image (square stamp)

    returns a 2D array with the PSF image
    '''
    
# using photoutils to find stars

    mean,median,std = sigma_clipped_stats(image, sigma = 3.0)
    print ((mean, median, std))
    
    daofind = DAOStarFinder(fwhm=3.0, threshold = 5*std, brightest = nstars)
    sources = daofind(image - median)
    for col in sources.colnames:
        sources[col].info.format = '%.8g'

    stack = []
    counter = 0	
    plt.figure(figsize=(10,6))
    for s in sources:
        x = s['xcentroid']
        y = s['ycentroid']
        xc,yc,xbox = x,y,size
        sample = [Cutout2D(image,(xc,yc),(xbox), mode = 'partial', fill_value = np.nan).data]
        sample = np.array(sample)
        sample = np.squeeze(sample)
#stacking images
        stack.append(sample)
# plotting the stars to check for overlap/poor quality images
        counter+=1
        plt.subplot(8,7,counter)
        plt.imshow(sample, origin = 'lower')
  
    print(np.shape(stack))
    plt.savefig('star_check.png',bbox_inches='tight')	
    plt.show()
# taking mean of stacked images                 
    mean = np.nanmean(stack,axis=0)
    print(mean.shape)

# measuring the psf	

    psf = mean

    return psf
