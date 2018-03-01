# MCMC model fitting

Before doing the task, it would be a good idea to [read this post](http://jakevdp.github.io/blog/2014/03/11/frequentism-and-bayesianism-a-practical-intro/). It looks really scary, but give it a try.

The task is to fit a straight line to data using MCMC. Try not to copy and paste Martin's code, but rather try to implement it yourself. The point is a better understanding of how it works.

`fitter.py` contains a function `fit_model` that takes a model (python function, which you can call as `model(x, k, m)`), data (x and y arrays) and an error on the y axis. The function should do the mcmc magic and return the two line parameters determined by a fit.

`run.py` is the file you want to run. It generates the data with gaussian noise, calls your `fit_model` function and plots the results. There are several parameters to change for testing purposes:

* `k, m` - line parameters
* `N` - number of data points to produce
* `err` - sigma of the gaussian noise
* `seed` - if 0, new set of datapoints is produced every time, if set to a number, the same one is produced
* `rng` - boundaries of the data in X axis