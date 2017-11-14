from __future__ import division
import numpy as np
from astropy import units as u


def simulate_light_curves(observation_times, lag, mean_continuum_flux, line_flux_ratio, log_gp_scale, log_gp_amplitude,
                          random_seed):
    """
    Creates three QSO light curves (continuum, pure emission line, combined emission line and continuum)
    :param observation_times:  astropy.Quantity (time)
    :param lag: astropy.Quantity (time)
    :param mean_continuum_flux:  astropy.Quantity (flux)
    :param line_flux_ratio:  astropy.Quantity (flux)
    :param log_gp_scale:  The scale of the gaussian process: float
    :param log_gp_amplitude: The amplitude of the gaussian process: float
    :param random_seed: int
    :return:
    """

    np.random.seed(random_seed)  # makes output deterministic


    ### your solution here
    ### instead of next line
    return [np.ones_like(observation_times.value) * i * u.mJy for i in range(3)]