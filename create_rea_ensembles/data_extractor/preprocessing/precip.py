import sys
import xarray as xr
import numpy as np

name_addition = ''
preprocessing_attr = 'precip = PRECC + PRECT'

def preprocessor(nc, *args):
    nc = nc.roll(lon=144, roll_coords=True)
    pr = nc['PRECC'] + nc['PRECL'] 
    pr *= 24*60*60 * 1000
    return xr.Dataset({'pr':pr})