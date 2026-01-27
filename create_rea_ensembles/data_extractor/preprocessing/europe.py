import sys
import xarray as xr
import numpy as np

name_addition = '-rbEU'
preprocessing_attr = 'big rectangle around Europe'

def preprocessor(nc):
    nc = nc.roll(lon=144, roll_coords=True)
    nc = nc.assign_coords(lon=(nc.lon + 180) % 360 - 180).sel(dict(lat=slice(10,80), lon=slice(-30,50)))
    return nc