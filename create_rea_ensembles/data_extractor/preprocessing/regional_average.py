import sys
import xarray as xr
import numpy as np
sys.path.append('../../')
from experiment_configuration.main_observable import create_or_load_regional_mask, shift_lon, regional_average

name_addition = '-reg'
preprocessing_attr = 'regional average over region of interest'

def preprocessor(nc, var_name):
    # regional mask
    regional_mask = create_or_load_regional_mask(
        regional_mask_file = f"/work/bb1152/u290372/GKLT/regions/wEU.nc",
        slice_lat=slice(44,55), 
        slice_lon=slice(-4,12),
        )

    nc = shift_lon(nc)
    return xr.Dataset({var_name:regional_average(nc[var_name], regional_mask)})
