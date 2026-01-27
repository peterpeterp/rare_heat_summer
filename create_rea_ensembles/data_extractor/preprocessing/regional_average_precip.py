import sys,importlib
import xarray as xr
import numpy as np
sys.path.append('../../')
from experiment_configuration.regions.region_by_slice import create_or_load_regional_mask, regional_average, shift_lon
from experiment_configuration.experiment import experiment

name_addition = '-reg'
preprocessing_attr = 'regional average over region of interest'

dummy_exp = experiment(importlib.import_module(f"experiment_configuration.c1").config)

def preprocessor(nc, *args):
    nc = shift_lon(nc)
    pr = nc['PRECC'] + nc['PRECL'] 
    pr *= 24*60*60

    # regional mask
    regional_mask = create_or_load_regional_mask(
        regional_mask_file = f"/work/bb1152/u290372/GKLT/regions/wEU.nc",
        slice_lat=slice(44,55), 
        slice_lon=slice(-4,12),
        )

    pr = regional_average(pr, regional_mask)
    return xr.Dataset({'pr':pr})
