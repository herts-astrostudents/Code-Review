from __future__ import division
import numpy as np
from astropy import units as u
import matplotlib.pyplot as plt

from solution import simulate_light_curves


observation_times = np.linspace(0, 500, 200) * u.day  # 200 observations over 500 days
lag = 100 * u.day
mean_flux = 10 * u.mJy
continuum, line, continuum_and_line = simulate_light_curves(observation_times,
                                                            lag=lag,
                                                            mean_continuum_flux=mean_flux,
                                                            line_flux_ratio=2*u.mJy,  # line is twice as strong as continuum
                                                            log_gp_scale=2,
                                                            log_gp_amplitude=0.4,
                                                            random_seed=0  # This is to get the same solution each time
                                                            )

plt.plot(observation_times, continuum.to(mean_flux.unit), linestyle='--', marker='o', label='continuum')
plt.plot(observation_times, line.to(mean_flux.unit), linestyle='--', marker='o', label='emission_line')
plt.plot(observation_times, continuum_and_line.to(mean_flux.unit), linestyle='--', marker='o',
         label='continuum + emission_line')
for i in np.arange(plt.xlim()[0], plt.xlim()[1], lag.value):
    plt.axvline(i, linestyle=':')
plt.legend()
plt.ylabel('flux / {}'.format(mean_flux.unit))
plt.xlabel('time / {}'.format(observation_times.unit))
plt.show()