import xarray as xr
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

def read_timestamp(fname):
    return np.datetime64(os.path.basename(fname).split('_')[1][:-4])


def read_file(fname):
    array = np.loadtxt(fname)
    return xr.DataArray(array)


def read_dated_file(fname):
    da = read_file(fname)
    time = read_timestamp(fname)
    return da.assign_coords(time=time)


def read_data(directory):
    fnames = [directory+'/'+i for i in os.listdir(directory)]
    times = set([read_timestamp(f) for f in  fnames])

    datasets = []

    for time in times:
        xc = read_dated_file(directory+'/xcoordinates_{}.txt'.format(time))
        yc = read_dated_file(directory+'/ycoordinates_{}.txt'.format(time))
        temp = read_dated_file(directory+'/airtemp_{}.txt'.format(time))
        
        ds = xr.Dataset({'temp': temp, 'xc': xc, 'yc': yc})
        ds = ds.rename({'dim_0': 'x', 'dim_1': 'y'})
        datasets.append(ds)
    return xr.concat(datasets, 'time')


def get_month_average_temp(dataset, month):
    """
    dataset: xr.Dataset: dataset object containing the 'temp' variable over time and space
    month: int: Month of the year
    """
    return dataset.groupby('time.month').mean('time').sel(month=month)


def plot_data(dataset, **kwargs):
    return dataset['temp'].plot(**kwargs)


def plot_temperature_map(dataset, month, **kwargs):
    month_data = get_month_average_temp(dataset, month)
    ax = kwargs.get('ax', plt.subplots()[1])
    return plot_data(month_data, ax=ax, **kwargs)