from __future__ import division
import numpy as np
from astropy import units as u


def random_walk(mean, times, amplitude, scale):
    deltas = times[1:] - times[:-1]
    deviate_variance = amplitude**2 * (1 - np.exp(-2 * deltas / scale))
    deviate = np.random.normal(0, np.sqrt(deviate_variance))  # truncate
    deviate = np.insert(deviate, 0, 0)
    alpha_ar = np.exp(-deltas / scale)
    
    for i, d in enumerate(deltas[1:], 1):
        deviate[i] += deviate[i-1] * alpha_ar[i]
    return deviate + mean



def simulate_light_curves(observation_times, lag, mean_continuum_flux, line_flux_ratio, log_gp_scale, log_gp_amplitude,
                          random_seed, coarseness=1/100/u.day):
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

    funit = mean_continuum_flux.unit
    gp_amplitude = 10**log_gp_amplitude
    gp_scale = 10**log_gp_scale

    step = min([min(observation_times[1:] - observation_times[:-1]), lag]) * coarseness
    mn, mx = min(observation_times) - lag, max(observation_times) + lag
    times = np.arange(mn.value, mx.value, step) * mx.unit

    print(times)

    _continuum_curve = random_walk(mean_continuum_flux.value, times.value, gp_amplitude, gp_scale)
    # _line_curve = np.interp(times, times-lag, _continuum_curve * line_flux_ratio)

    continuum_curve = np.interp(observation_times, times, _continuum_curve)
    line_curve = np.interp(observation_times, times-lag, _continuum_curve)
    line_and_continuum_curve = continuum_curve + line_curve
    
    return continuum_curve * funit, line_curve * funit, line_and_continuum_curve * funit