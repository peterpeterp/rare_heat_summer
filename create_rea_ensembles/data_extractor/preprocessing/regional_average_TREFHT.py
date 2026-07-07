import sys
import xarray as xr
import numpy as np
sys.path.append('../../')
from experiment_configuration.main_observable import create_or_load_regional_mask, shift_lon, regional_average

name_addition = '-reg'
preprocessing_attr = 'regional average over region of interest'

def preprocessor(nc, *args):
    # regional mask
    regional_mask = create_or_load_regional_mask(
        regional_mask_file = f"regional_mask.nc",
        slice_lat=slice(44,55), 
        slice_lon=slice(-4,12),
        )

    nc = shift_lon(nc)
    x = regional_average(nc['TREFHT'], regional_mask)
    x -= 273.15
    return xr.Dataset({'TREFHT':x})
