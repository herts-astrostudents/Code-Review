# Bootstrap

This is a simple task to understand usage of bootstrap.

Write the code in `solution.py`, as usual.
The function `bootstrap_this(data)` in `solution.py` takes one argument - an array of measurements of equivalent width of the NaD1 line in Alpha Centauri B over the last 10 years. We want to get the mean value and estimate the error on it using bootstrap, as the distribution of measurements is unknown. This dataset is used just as an example, so it doesn't really matter what it is.

Bootstrap works by using the dataset itself to estimate the distribution. You make many new samples by drawing new datasets from the old ones, with replacement, and re-measuring the statistic. The distribution of the statistic is then an approximation to the one it would have if you were to repeat the experiment.

In other words, you randomly draw N values from the array of N elements (some of them repeat), calculate mean and repeat 100-10000 times. As a result you get a distribution of mean values, from which you measure mean and error and return them along with all the means.

`run.py` is the file you want to run - it reads the data, runs your function and shows the result.

Feel free to write your own bootstrap routineor make use of some packages, there are many ways to do it.


<img src="sample_output.png" alt="sample output"/>