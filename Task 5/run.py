from numpy import exp, random, sort, linspace
import matplotlib.pyplot as plt
from fitter import fit_model


def line(x, k, m):
	return k*x + m

def generate_data(k=1.0, m=1.0, n=100, err=1, seed=0, rng=[0, 10]):
	if seed:
		random.seed(seed)

	# get unevenly spaced X array
	x = sort(random.uniform(rng[0], rng[1], size=(n,)))

	# get Y values
	y = line(x, k, m)

	# get gaussian noise
	delta = random.normal(0, err, size=(n,))

	return x, y+delta, err*3


k  = -0.2
m = 1.8
N = 12
err = 0.1
seed = 0
rng = (-1, 3)


x, y, yerr = generate_data(k, m, n=N, err=err, seed=seed, rng=rng)
xlin = linspace(min(x), max(x), 100)


k_fit, m_fit = fit_model(line, x, y, yerr)

plt.plot(xlin, line(xlin, k, m), label='original', color='#3F681C', linestyle='--', alpha=0.8)
plt.errorbar(x, y, yerr=yerr, label='data', linestyle='none', marker='o', color='#375E97', alpha=0.8)
plt.plot(xlin, line(xlin, k_fit, m_fit), label='model fit', color='#FB6542', linestyle='-')
plt.legend()
plt.show()