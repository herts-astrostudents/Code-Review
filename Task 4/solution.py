import numpy as np

from utilities import log_OIII_Hb_NII, log_OIII_Hb_NII_lower, log_OIII_Hb_NII_upper, WIDTH, ASYMPTOTE


def solution(data):
    data['BPT_Y'] = np.log10(data['OIII_FLUX'] / data['H_BETA_FLUX'])
    data['BPT_X'] = np.log10(data['NII_6584_FLUX'] / data['H_ALPHA_FLUX'])
    data['is_5_sigma'] = True
    for colname in data.colnames:
        if ('FLUX' in colname) and ('ERR' not in colname):
            data[colname+'_SNR'] = data[colname] / data[colname+'_ERR']
            data['is_5_sigma'] &= data[colname+'_SNR'] > 5

    data['BPT_class'] = 'Composite'
    data['BPT_class'][data['BPT_Y'] < log_OIII_Hb_NII_lower(data['BPT_X'])] = 'SFG'
    data['BPT_class'][data['BPT_Y'] > log_OIII_Hb_NII_upper(data['BPT_X'])] = 'AGN'
    data['BPT_class'][data['BPT_X'] > 0.47-0.1] = 'AGN'
    return data
