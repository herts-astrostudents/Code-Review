from astropy.table import Table, unique
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from utilities import log_OIII_Hb_NII, log_OIII_Hb_NII_upper, log_OIII_Hb_NII_lower, ASYMPTOTE, WIDTH
from solution import solution


def plot_bpt(table):
	for classification in set(table['BPT_class'].data):
		d = table[table['BPT_class'] == classification]
		plt.scatter(d['BPT_X'], d['BPT_Y'], s=3, alpha=0.5, label=classification)

	plt.legend()
	ylim = plt.ylim()
	xlim = plt.xlim()
	x = np.linspace(*xlim, num=1000)
	plt.plot(x[x < ASYMPTOTE], log_OIII_Hb_NII(x[x < ASYMPTOTE]), 'k-')
	plt.plot(x[x < ASYMPTOTE+WIDTH], log_OIII_Hb_NII_upper(x[x < ASYMPTOTE+WIDTH]), 'k--')
	plt.plot(x[x < ASYMPTOTE-WIDTH], log_OIII_Hb_NII_lower(x[x < ASYMPTOTE-WIDTH]), 'k--')
	plt.xlim(xlim)
	plt.ylim(ylim)
	plt.xlabel(r'$log_{10}[NII / H\alpha]$')
	plt.ylabel(r'$log_{10}[OIII / H\beta]$')



data = solution(Table(fits.open(r'data.fits')[1].data))
plot_bpt(data[data['is_5_sigma']])
plt.show()
