from astropy.stats import sigma_clipped_stats
from astropy.nddata import Cutout2D
from photutils import DAOStarFinder
import numpy as np

import matplotlib.pyplot as plt
from astropy.table import Table

#from astropy.visualization import SqrtStretch
#from astropy.visualization.mpl_normalize import ImageNormalize

def distance(x1, y1, x2, y2):
    """
    Distance in pixel between two sources
    """     
    return np.sqrt( (x1 - x2)**2 + (y1 - y2)**2 )
 
    
def pick_value(value, array, threshold): 
    """
    To find the index of the closest array member to a given value
    """  
    i=0
    while np.abs(array[i]-value) > threshold:
        i = i+1
    return i 
    

def estimate_psf(image, nstars=10, size=20): # I assume the image is f[0].data (f = fits.open(...))
    '''
    Estimate an empirical psf from the image

    image: 2D array, image with some stars
    nstars: int, number of brightest stars to stack
    size: int, size of the resulting PSF image (square stamp)

    returns a 2D array with the PSF image
    '''

    # 1) Estimate the background and background noise using sigma-clipped statistics,
# substrack the background

    data = image
    mean, median, std = sigma_clipped_stats(data, sigma=3.0, iters=5)
#    print((mean, median, std))
    data_ok = data - median #I substrack the background noise


# 2) Now we will use an instance of DAOStarFinder to find the stars in the image 
#that have FWHMs of around 3 pixels and have peaks approximately 10-sigma above the background. 
    daofind = DAOStarFinder(fwhm=3.0, threshold=10.*std)  
    sources_all = daofind(data_ok)
    for col in sources_all.colnames:    
        sources_all[col].info.format = '%.8g'  # for consistent table output    

# 3) But the stars have to be sufficiently separated, so we exclude some of them
    thres = 20
    sources = daofind(data_ok)

    for i in range(len(sources_all)):
        for j in range(i+1, len(sources_all)):
            if distance(sources_all[i]['xcentroid'], sources_all[i]['ycentroid'], sources_all[j]['xcentroid'], sources_all[j]['ycentroid']) < thres:
                try:
                    ind = pick_value(sources_all[j]['xcentroid'], sources['xcentroid'], 0.1)
                    ind2 = pick_value(sources_all[i]['xcentroid'], sources['xcentroid'], 0.1)
                    sources.remove_row(ind)
                    sources.remove_row(ind2)
                except IndexError:    #sometimes I get an error, I don't know why
                    pass 
                
##Plot the image and the stars
#    plt.figure(1)
#    plt.clf()
#
#    from photutils import CircularAperture
#    positions = (sources['xcentroid'], sources['ycentroid'])
#    apertures = CircularAperture(positions, r=4.)
#    norm = ImageNormalize(stretch=SqrtStretch())
#    plt.imshow(np.log10(data), cmap='Greys', origin='lower', norm=norm)
#    apertures.plot(color='blue', lw=1.5, alpha=0.5) # I plot blue apertures only in the selected stars
#
#    positions2 = (sources_all['xcentroid'], sources_all['ycentroid'])
#    apertures2 = CircularAperture(positions2, r=4.)
#    apertures2.plot(color='red', lw=1.5, alpha=0.5) #I plot red apertures for all the stars, so the selected stars are the purple apertures   

                
# 4) Now let's extract the selected stars
    from astropy.nddata import NDData
    nddata = NDData(data=data_ok) #the extract_stars function requires the input data as an NDData object
    stars_tbl = Table() #and also requires a table of star positions in either pixel or sky coordinates
    stars_tbl['x'] = sources['xcentroid']
    stars_tbl['y'] = sources['ycentroid']
# To extract 25 x 25 pixel cutouts of our selected stars:
    from photutils.psf import extract_stars   
    stars = extract_stars(nddata, stars_tbl, size=25)    
## Let's show the first 25 stars
#    from astropy.visualization import simple_norm
#    nrows = 5
#    ncols = 5
#    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(20, 20), squeeze=True)
#    ax = ax.ravel()
#    for i in range(nrows*ncols):
#        norm = simple_norm(stars[i], 'log', percent=99.)
#        ax[i].imshow(stars[i], norm=norm, origin='lower', cmap='viridis')

# Other way to do this: (with Cutout2D)
#pos_tuple = tuple(zip(sources['xcentroid'], sources['ycentroid']))
#size = (25,25)
#stars2 = Cutout2D(data_ok, pos_tuple, size) #not working, I don't know why ??????????????????????????????????????????????/   
#  

# 5) Now we stack the selected stars together with the mean to build the psf
    for i in range(stars.n_all_stars):
        stacked=+stars.all_good_stars[i].data

    psf = stacked / stars.n_all_stars   
        
        
    return psf
