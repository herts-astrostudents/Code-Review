from astropy.table import Table
from spectrum import Spectrum
from filters import Filter
from diagram import ColourColourDiagram
import matplotlib.pyplot as plt

table = Table.read('sdss_data.fits')  # magnitudes from SDSS so that we can classify our spectrum
stars = table[table['class'] == 'STAR']
qsos = table[table['class'] == 'QSO']

# read in the relevant filter curves
u_filter = Filter.from_file('sdss_filters/sdss-u.fits')
g_filter = Filter.from_file('sdss_filters/sdss-g.fits')
r_filter = Filter.from_file('sdss_filters/sdss-r.fits')

# Now define our colours using filters
# Python allows us to decide how objects use the `-` operator. Look at `Filter` to see how it works
ug_colour = u_filter - g_filter
gr_colour = g_filter - r_filter

star_galaxy_diagram = ColourColourDiagram(ug_colour, gr_colour)  # make a colour-colour diagram using the two colours above
star_galaxy_diagram.plot_table(stars, c='b', alpha=0.2, s=1, label='stars')  # plot the known stars using the `plot_table` method
star_galaxy_diagram.plot_table(qsos, c='r', alpha=0.2, s=1, label='QSOs')  # plot the known qsos using the `plot_table` method

spectrum = Spectrum.from_file('spec-0266-51602-0003.fits')  # read the spectrum into the `Spectrum` object
star_galaxy_diagram.plot_spectrum(spectrum, c='k', s=50)  # plot the spectrum, where all the maths is behind the scenes

# So you can see that it is now really easy to plot any additional spectra we have without changing your code

plt.legend()
plt.show()