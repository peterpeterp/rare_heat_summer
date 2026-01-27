import sys,importlib
import xarray as xr
import numpy as np
sys.path.append('../../')
from experiment_configuration.regions.region_by_slice import create_or_load_regional_mask, regional_average, shift_lon
from experiment_configuration.experiment import experiment

name_addition = '-reg'
preprocessing_attr = 'regional average over region of interest'

dummy_exp = experiment(importlib.import_module(f"experiment_configuration.c1").config)

def preprocessor(nc):
    nc = shift_lon(nc)
    obs = nc['SOILWATER_10CM']
    obs = regional_average(obs, dummy_exp.regional_mask)
    return obs
