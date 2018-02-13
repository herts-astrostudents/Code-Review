import numpy as np

from utilities import log_OIII_Hb_NII, log_OIII_Hb_NII_lower, log_OIII_Hb_NII_upper, WIDTH, ASYMPTOTE


def solution(data, sigma=5):
    """
    Works out BPT quantities for plotting
    :param data: astropy.table.Table : Contains the FLUX and FLUX_ERR columns for OIII, NII_6584, H_ALPHA, H_BETA
    :param sigma: add a column named 'is_{sigma}_sigma' which contains True for rows which have all BPT lines @ {sigma} sigma
    :return: same astropy.table.Table with added BPT columns
    """
    data['BPT_Y'] = np.log10(data['OIII_FLUX'] / data['H_BETA_FLUX'])
    data['BPT_X'] = np.log10(data['NII_6584_FLUX'] / data['H_ALPHA_FLUX'])
    sigma_col = 'is_{}_sigma'.format(sigma)
    data[sigma_col] = True  # use logical_and later to combine line SNR conditions
    for colname in data.colnames:
        if ('FLUX' in colname) and ('ERR' not in colname):
            data[colname+'_SNR'] = data[colname] / data[colname+'_ERR']
            data[sigma_col] &= data[colname+'_SNR'] > sigma

    # move along the x direction to eventually cover all space
    data['BPT_class'] = 'Composite'  # easier to predefine everything as Composite and then change them
    data['BPT_class'][data['BPT_Y'] < log_OIII_Hb_NII_lower(data['BPT_X'])] = 'SFG'
    data['BPT_class'][data['BPT_Y'] > log_OIII_Hb_NII_upper(data['BPT_X'])] = 'AGN'
    data['BPT_class'][data['BPT_X'] > ASYMPTOTE-WIDTH] = 'AGN'  # anything to right is now AGN (everything is covered)
    return data
