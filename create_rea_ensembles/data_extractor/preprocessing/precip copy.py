import sys
import xarray as xr
import numpy as np

name_addition = '-rbEU'
preprocessing_attr = 'big rectangle around Europe'

def preprocessor(nc):
    nc = nc.roll(lon=144, roll_coords=True)
    pr = nc['PRECC'] + nc['PRECL'] 
    pr *= 24*60*60 * 1000
    return xr.Dataset({'pr':pr})