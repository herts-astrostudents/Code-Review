from matplotlib import pyplot as plt
import numpy as np

from data import fetch_sdss_filter, fetch_vega_spectrum

fig, ax = plt.subplots()

#----------------------------------------------------------------------
# Fetch and plot the Vega spectrum
#----------------------------------------------------------------------

filters = ['u','g','r','i','z']
colours = ['blue','green','red','purple','black']

sdss = [fetch_sdss_filter(a) for a in filters]
for i in range(5):
	plt.fill(sdss[i][0],sdss[i][1]*2, c = colours[i],alpha = 0.4, linewidth = 0)
	plt.gca().text(np.mean(sdss[i][0]), 0.05, '{}'.format(filters[i]), color = colours[i], fontweight = 'bold', fontsize = '14', va = 'center', ha = 'center')
vega = fetch_vega_spectrum()

### Normalise vega spectrum
vega[1] = vega[1] / max(vega[1]) 

plt.plot(vega[0], vega[1], c = 'k', linewidth = 2)


plt.gca().set_xlim(3000,11000)
plt.show()
