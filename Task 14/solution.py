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
    """
    saves x and y co-ords and monthly average temperature fields in "dataset"
    """
    # load file names
    fnames = [directory+'/'+i for i in os.listdir(directory)]
    # list years and months to scan
    years = ['1980','1981','1982','1983'] 
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    # predefine arrays to use
    tmp         = np.loadtxt(fnames[0])
    t_final     = np.zeros((12,tmp.shape[0],tmp.shape[1]))
    x_final     = np.zeros((12,tmp.shape[0],tmp.shape[1]))
    y_final     = np.zeros((12,tmp.shape[0],tmp.shape[1]))
    count_month = 0
    dataset     = []
    # loop through months to find average temperatures
    for month in months:
        # predefine arrays for each loop
        temps      = np.zeros(tmp.shape)
        count_year = 0
        # loop through years to find all data for current month
        for year in years:
            # date string to search for files for current month
            date_string = year + '-' + month
            # find files for current month
            for fname in fnames:
                if date_string in fname: 
                    if 'airtemp' in fname:
                        file_at = fname
                    if 'xcoordinates' in fname:
                        file_x = fname
                    if 'ycoordinates' in fname:
                        file_y = fname
            # "try" here because not all months have files in every year
            try:
                file_at
            except: 
                None
            else: # if files exist then add temps from current month each year
                if count_year is 1:
                    blah = temps
                temps = temps + np.loadtxt(file_at)
                count_year = count_year + 1
                
            try:
                file_x
            except: 
                None
            else: # save x, although have not used it
                xs = np.loadtxt(file_x)
                
            try:
                file_y
            except: 
                None
            else: # ditto with y
                ys = np.loadtxt(file_y)
        # append fields for each month to a dataset        
        dataset.append({"t":temps/count_year,"x":xs,"y":ys})

    return dataset  # dataset might be an xarray.Dataset object or a clever structure of arrays 


def plot_data(dataset, **kwargs):
    """
    plots temperature over x and y for a single time (i.e. dataset should consist of 1 time)
    """
    
    cmap = kwargs["cmap"]
    tlim = np.nanmax(np.abs(dataset["t"]))
    
    #mp = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')
    #mp = Basemap(projection='ortho',lon_0=-105,lat_0=40,resolution='l')
    #mp = Basemap(width=12000000,height=9000000,projection='lcc',resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
    #x, y = mp(dataset["x"],dataset["y"])
    #plt.pcolormesh(x,y,dataset["t"],cmap=cmap,vmin=-tlim,vmax=tlim)
    
    #plt.pcolormesh(dataset["x"],dataset["y"],dataset["t"],cmap=cmap,vmin=-tlim,vmax=tlim)
    
    plt.pcolormesh(dataset["t"],cmap=cmap,vmin=-tlim,vmax=tlim)
    
    plt.colorbar()


def plot_temperature_map(dataset, month, **kwargs):
    month_data = dataset[month-1]
    ax = kwargs.get('ax', plt.subplots()[1])  # all this does is get make an axis if you haven't given the function ax=(an axis)
    return plot_data(month_data, ax=ax, **kwargs)  # kwargs holds the optional colormap and other arguments as a dictionary