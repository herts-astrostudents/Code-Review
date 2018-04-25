from matplotlib import pyplot as plt
import numpy as np

from data import fetch_sdss_filter, fetch_vega_spectrum
from style import stylise_pyplot


class Spectrum(object):
	def __init__(self, wl, fl, colour='#04202c', normalise=False):
		self.wl = wl
		self.fl = fl
		self.colour = colour
		if normalise == True:
			self.__normalise()

	def __normalise(self, range=[0, 1]):
		mn = min(self.fl)
		mx = max(self.fl)
		self.fl = (self.fl-mn)/(mx-mn)


# get the data
spectrum = Spectrum(*fetch_vega_spectrum(), colour='#04202c', normalise=True)
filters = {
	'u' : Spectrum(*fetch_sdss_filter('u')[0:2], colour='#283655', normalise=False),
	'g' : Spectrum(*fetch_sdss_filter('g')[0:2], colour='#20948B', normalise=False),
	'r' : Spectrum(*fetch_sdss_filter('r')[0:2], colour='#DE7A22', normalise=False),
	'i' : Spectrum(*fetch_sdss_filter('i')[0:2], colour='#8D230F', normalise=False),
	'z' : Spectrum(*fetch_sdss_filter('z')[0:2], colour='#867666', normalise=False),
}


# plot the data
fig, ax = plt.subplots()
ax2 = ax.twinx() # secondary scale for the filters
stylise_pyplot(plt)


filter_alpha = 0.5
for name in filters:
	ax2.fill(filters[name].wl, filters[name].fl, color=filters[name].colour, alpha=filter_alpha)
	ax2.plot(filters[name].wl, filters[name].fl, color=filters[name].colour)
	plt.text(np.average(filters[name].wl, weights=filters[name].fl), 0.05, name, fontsize=18, color=filters[name].colour)

ax.plot(spectrum.wl, spectrum.fl, c=spectrum.colour, linewidth=2, label='Vega')


# move x ticks lower to avoid overlap at the origin
for tick in ax.get_xaxis().get_major_ticks():
    tick.set_pad(8.)

ax.set_xlim(3000, 11000)
ax.legend(loc='upper right')
ax.set_xlabel('Wavelength, Angstrom')
ax.set_ylabel('Normalised flux')
ax.set_title('SDSS filters and reference spectrum')
ax2.set_ylabel('Filter transmission')


plt.show()