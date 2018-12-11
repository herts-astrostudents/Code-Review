try:
    import xarray as xr
except ImportError:
    print("It is advisable to use xarray, but you can still use numpy if you want")
import numpy as np
import os
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap


# this allows you to read timestamps properly from a filename
# datatime64 objects store the month, day, second etc so you can access them
def read_timestamp(fname):
    return np.datetime64(os.path.basename(fname).split('_')[1][:-4])


def read_data(directory):
    fnames = [directory+'/'+i for i in os.listdir(directory)]
    
    years = ['1980','1981','1982','1983']
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    
    tmp   = np.loadtxt(fnames[0])
    t_final = np.zeros((12,tmp.shape[0],tmp.shape[1]))
    x_final    = np.zeros((12,tmp.shape[0],tmp.shape[1]))
    y_final    = np.zeros((12,tmp.shape[0],tmp.shape[1]))
    
    count_month = 0
    dataset = []
    
    for month in months:
        
        temps = np.zeros(tmp.shape)
        count_year = 0
        
        for year in years:
            
            date_string = year + '-' + month
            
            for fname in fnames:
                if date_string in fname: 
                    if 'airtemp' in fname:
                        file_at = fname
                    if 'xcoordinates' in fname:
                        file_x = fname
                    if 'ycoordinates' in fname:
                        file_y = fname
            
            try:
                file_at
            except: 
                None
            else:
                if count_year is 1:
                    blah = temps
                temps = temps + np.loadtxt(file_at)
                count_year = count_year + 1
                
            try:
                file_x
            except: 
                None
            else:
                xs = np.loadtxt(file_x)
                
            try:
                file_y
            except: 
                None
            else:
                ys = np.loadtxt(file_y)
                
        dataset.append({"t":temps/count_year,"x":xs,"y":ys})

    return dataset  # dataset might be an xarray.Dataset object or a clever structure of arrays 


def plot_data(dataset, **kwargs):
    """
    plots temperature over x and y for a single time (i.e. dataset should consist of 1 time)
    """
    plt.pcolormesh(dataset["x"],dataset["y"],dataset["t"])


def plot_temperature_map(dataset, month, **kwargs):
    month_data = dataset[month-1]
    ax = kwargs.get('ax', plt.subplots()[1])  # all this does is get make an axis if you haven't given the function ax=(an axis)
    return plot_data(month_data, ax=ax, **kwargs)  # kwargs holds the optional colormap and other arguments as a dictionary