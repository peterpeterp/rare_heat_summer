import os,sys,glob
import xarray as xr
import numpy as np

import regionmask

name_addition = '-atl'
preprocessing_attr = 'regional average over the Atlantic sector (30N-70N and 80W-10W)'


def shift_lon(nc):
    nc.coords['lon'] = (nc.coords['lon'] + 180) % 360 - 180
    nc = nc.sortby(nc.lon)
    return nc

def preprocessor(nc, *args):
    nc = shift_lon(nc)
    nc = nc.sel(dict(lat=slice(30,70), lon=slice(-80,-10)))
    x = nc['U500'].weighted(np.cos(np.radians(nc.lat))).mean(('lat','lon'))
    return xr.Dataset({'U500':x})