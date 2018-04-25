from matplotlib import pyplot as plt
import numpy as np

from data import fetch_sdss_filter, fetch_vega_spectrum

fig, ax = plt.subplots()

#----------------------------------------------------------------------
# Fetch and plot the Vega spectrum

spectrum = fetch_vega_spectrum()
lam = spectrum[0]
flux = spectrum[1] / spectrum[1].max()
ax.plot(lam, flux, '-k', lw=2, label='Vega')

#------------------------------------------------------------
# Fetch and plot the five filters
text_kwargs = dict(fontsize=20, ha='center', va='center', alpha=0.5)

filter_ax = ax.twinx()
for f, c in zip('ugriz', 'bgrmk'):
    data = fetch_sdss_filter(f)
    loc = np.average(data[0], weights=data[1])
    filter_ax.fill(data[0], data[1], ec=c, fc=c, alpha=0.4)
    filter_ax.text(loc, 0.02, f, color=c, **text_kwargs)

ax.set_xlim(3000, 11000)
filter_ax.set_ylabel('Filter transmission')
ax.set_ylim(0, 1)
filter_ax.set_ylim(0, filter_ax.get_ylim()[1])

ax.set_title('SDSS Filters and Reference Spectrum')
ax.set_xlabel('Wavelength (Angstroms)')
ax.set_ylabel('Normalised flux')
ax.legend()

plt.show()
