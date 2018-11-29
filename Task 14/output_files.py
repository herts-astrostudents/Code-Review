import xarray as xr
import numpy as np

ds = xr.tutorial.load_dataset('rasm')

for t in ds.time.values:
    sub = ds.sel(time=t)
    np.savetxt("data/airtemp_{}.txt".format(t), sub['Tair'].values)
    np.savetxt("data/xcoordinates_{}.txt".format(t), sub['xc'].values)
    np.savetxt("data/ycoordinates_{}.txt".format(t), sub['yc'].values)