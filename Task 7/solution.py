from matplotlib import pyplot as plt
import numpy as np

from data import fetch_sdss_filter, fetch_vega_spectrum

#----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(4,4))

#----------------------------------------------------------------------
# Fetch and plot the Vega spectrum
bands = ['u', 'g', 'r', 'i', 'z']
colour = ['blue', 'green', 'red', 'purple', 'black']
for band, col in zip(bands, colour):
    wavelength = fetch_sdss_filter(band)[0]
    response = fetch_sdss_filter(band)[1]
    ax.fill_between(wavelength, y1=response, y2=0, alpha=0.35, color=col)
    ax.text(np.average(wavelength, weights=response), 0.02, band, color=col, fontsize=20, va='center')
wavelength, flux = fetch_vega_spectrum()
ax2 = ax.twinx()
ax2.plot(wavelength, flux/np.max(flux), linewidth=2, color='k', label='Vega')

ax.set_xlim(3000,11000)
ax.set_ylim(0,0.5)
ax2.set_xlim(3000,11000)
ax2.set_ylim(0,1)

ax2.legend()

ax2.set_ylabel('Normalised flux')
ax.set_ylabel('Filter transmission')
ax.set_xlabel('Wavelelength / Angstroms')

plt.show()