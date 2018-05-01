import numpy as np
import matplotlib.pyplot as plt
from solution import bootstrap_this

def get_hist(x, bins=100):
	hist, bins = np.histogram(x, bins=bins)
	centers = [np.mean([bins[i], bins[i-1]]) for i in range(1, len(bins))]
	return centers, hist

# read the data
print('reading data...')
data = np.genfromtxt('ew.dat')

fig, ax = plt.subplots(2, 1, figsize=(11,8))

# plot the distribution
ax[0].hist(data, bins=50, color='#556dac')
ax[0].set_xlabel('measurements')
ax[0].set_ylabel('N')

# the solution
print('bootstrapping...')
value, error, means = bootstrap_this(data)

# plot results
ax[1].hist(means, bins=50, color='#556dac')

ax[1].axvline(value, c='#283655', linewidth=2, label='Mean: ' + "{:.4f}".format(value))
ax[1].axvline(value-error, c='#ed5752', linewidth=2, label='Error: ' + "{:.4f}".format(100*error/value) + '%' )
ax[1].axvline(value+error, c='#ed5752', linewidth=2)
ax[1].set_xlim(value-error*5, value+error*5)
ax[1].set_xlabel('mean values')
ax[1].set_ylabel('N')
ax[1].legend(loc='upper right')

print('Done')
plt.savefig('sample_output.png')
plt.show()
