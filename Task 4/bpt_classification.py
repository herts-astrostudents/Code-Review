from astropy.table import Table
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt








data = Table(fits.open(r'data.fits')[1].data)

data['BPT_Y'] = np.log10(data['OIII_FLUX'] / data['H_BETA_FLUX'])
data['BPT_X'] = np.log10(data['NII_6584_FLUX'] / data['H_ALPHA_FLUX'])
data['is_5sigma'] = True
for colname in data.colnames[:-3]:
    if 'ERR' not in colname:
        data[colname+'_SNR'] = data[colname] / data[colname+'_ERR']
        data['is_5sigma'] &= data[colname+'_SNR'] > 5

d = data[data['is_5sigma']]
plt.scatter(d['BPT_X'], d['BPT_Y'], s=3, alpha=0.5)
ylim = plt.ylim()
xlim = plt.xlim()
x = np.linspace(*ylim)
plt.plot(x, log_OIII_Hb_NII(x))
plt.plot(x, log_OIII_Hb_NII(x, 0.1))
plt.plot(x, log_OIII_Hb_NII(x, -0.1))
plt.xlim(xlim)
plt.ylim(ylim)
plt.show()