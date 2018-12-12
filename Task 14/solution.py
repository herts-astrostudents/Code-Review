try:
    import xarray as xr
except ImportError:
    print("It is advisable to use xarray, but you can still use numpy if you want")
import numpy as np
import os
import matplotlib.pyplot as plt
import datetime


# this allows you to read timestamps properly from a filename
# datatime64 objects store the month, day, second etc so you can access them
def read_timestamp(fname):
    timestamp_string = os.path.basename(fname).split('_')[1][:-7]
    return datetime.datetime.strptime(timestamp_string, "%Y-%m-%dT%H:%M:%S.%f")


def read_data(directory):
    fnames = [directory + '/' + i for i in os.listdir(directory)]

    timestamps   = np.array([read_timestamp(fname) for fname in fnames if 'airtemp' in fname])
    airtemps     = np.array([np.loadtxt(fname, delimiter=' ', unpack=True) for fname in fnames if 'airtemp'      in fname])
    xcoordinates = np.array([np.loadtxt(fname, delimiter=' ', unpack=True) for fname in fnames if 'xcoordinates' in fname])
    ycoordinates = np.array([np.loadtxt(fname, delimiter=' ', unpack=True) for fname in fnames if 'ycoordinates' in fname])

    return {
        'timestamps'   : timestamps,
        'airtemps'     : airtemps,
        'xcoordinates' : xcoordinates,
        'ycoordinates' : ycoordinates,
    }  # dataset might be an xarray.Dataset object or a clever structure of arrays 


def get_month_average_temp(dataset, month, average_function=np.mean):
    """
    dataset: xr.Dataset: dataset object containing the 'temp' variable over time and space
    month: int: Month of the year
    """
    
    mask = np.array([dt.month == month for dt in dataset['timestamps']])
    dataset['timestamps']   = dataset['timestamps'  ][mask]
    dataset['airtemps']     = dataset['airtemps'    ][mask]
    dataset['xcoordinates'] = dataset['xcoordinates'][mask]
    dataset['ycoordinates'] = dataset['ycoordinates'][mask]

    print(month, mask)
    averaged_dataset = {
        'month'        : month, 
        'airtemps'     : np.array(average_function(dataset['airtemps'],     axis=0)),
        'xcoordinates' : np.array(average_function(dataset['xcoordinates'], axis=0)),
        'ycoordinates' : np.array(average_function(dataset['ycoordinates'], axis=0)),
    }

    return averaged_dataset  # averaged_dataset might also be an xarray.Dataset object or a clever structure of arrays 


def plot_data(dataset, **kwargs):
    """
    plots temperature over x and y for a single time (i.e. dataset should consist of 1 time)
    """
    ax = kwargs.pop('ax')
    ax.set_title("month = {}".format(dataset['month']))
    
    # PCOLORMESH
    # cm = ax.pcolormesh(dataset['xcoordinates'], dataset['ycoordinates'], dataset['airtemps'], **kwargs)
    # IMSHOW
    cm = ax.imshow(dataset['airtemps'], aspect="equal", **kwargs)
    
    plt.colorbar(cm, ax=ax)


def plot_temperature_map(dataset, month, **kwargs):
    month_data = get_month_average_temp(dataset, month)
    ax = kwargs.get('ax', plt.subplots()[1])  # all this does is get make an axis if you haven't given the function ax=(an axis)
    return plot_data(month_data, ax=ax, **kwargs)  # kwargs holds the optional colormap and other arguments as a dictionary