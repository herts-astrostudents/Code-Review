try:
    import xarray as xr
except ImportError:
    print("It is advisable to use xarray, but you can still use numpy if you want")
import numpy as np
import os
import matplotlib.pyplot as plt


# this allows you to read timestamps properly from a filename
# datatime64 objects store the month, day, second etc so you can access them
def read_timestamp(fname):
    return np.datetime64(os.path.basename(fname).split('_')[1][:-4])


def read_data(directory):
    fnames = [directory+'/'+i for i in os.listdir(directory)]

    # do your stuff here

    return dataset  # dataset might be an xarray.Dataset object or a clever structure of arrays 


def get_month_average_temp(dataset, month):
    """
    dataset: xr.Dataset: dataset object containing the 'temp' variable over time and space
    month: int: Month of the year
    """

    # do your stuff here

    return averaged_dataset  # averaged_dataset might also be an xarray.Dataset object or a clever structure of arrays 


def plot_data(dataset, **kwargs):
    """
    plots temperature over x and y for a single time (i.e. dataset should consist of 1 time)
    """
    # do you stuff here


def plot_temperature_map(dataset, month, **kwargs):
    month_data = get_month_average_temp(dataset, month)
    ax = kwargs.get('ax', plt.subplots()[1])  # all this does is get make an axis if you haven't given the function ax=(an axis)
    return plot_data(month_data, ax=ax, **kwargs)  # kwargs holds the optional colormap and other arguments as a dictionary