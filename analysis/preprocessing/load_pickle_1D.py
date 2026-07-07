import os,sys,subprocess,glob,importlib,pickle,itertools
import datetime
import xarray as xr
import numpy as np
import pandas as pd
import scipy,math
import seaborn as sns

sys.path.append('../')
from sup.useful_functions import *

#sys.path.append('../REA_with_CESM2')
#from ensembles.ensemble_GKLT import ensemble_GKLT,get_weight_for_selection

sys.path.append('/home/u/u290372/projects/REA_heat_wEU_JJA')
sys.path.append('/home/peterp/projects/REA_heat_wEU_JJA')
from experiment_configuration.experiment import experiment

def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

climates = ['ssp370-2025', 'piControl']

def prep_data(path='pickles/REA_heat_1D.pkl'):
    with open(path, 'rb') as fl:
        ensembles = pickle.load(fl)
        

    for i,j in enumerate(list(range(1,6)) + [10]):
        exp = experiment(import_from(f'experiment_configuration.c{j}', 'config'), online=False)
        old_ens_name = f"{exp.initial_conditions_name}-x{exp.experiment_new_identifier}"
        new_ens_name = f"{exp.initial_conditions_name}-x{i+1}"
        ens = ensembles[old_ens_name].copy()
        ensembles.pop(old_ens_name)
        ensembles[new_ens_name] = ens
        ens['exp'] = exp
        
    for i,j in enumerate(range(1,7)):
        exp = experiment(import_from(f'experiment_configuration.p{j}', 'config'), online=False)
        old_ens_name = f"{exp.initial_conditions_name}-x{exp.experiment_new_identifier}"
        new_ens_name = f"{exp.initial_conditions_name}-x{i+1}"
        ens = ensembles[old_ens_name].copy()
        ensembles.pop(old_ens_name)
        ensembles[new_ens_name] = ens
        ens['exp'] = exp

    for experiment_identifier in ['c7_dry','c8_dry','c6_dry','c9_dry', 'c11_dry', 'c12_dry']:
        exp = experiment(import_from(f'experiment_configuration.{experiment_identifier}', 'config'), online=False)
        ensembles[f"{exp.initial_conditions_name}-x{exp.experiment_new_identifier}"]['exp'] = exp

    for climate in climates:
        for ens_name, ens in ensembles.items():
            if climate in ens_name and 'initial' not in ens_name and 'wet' not in ens_name and 'dry' not in ens_name:
                ensembles[f"{climate}-initial"]['exp'] = ens['exp']

    for climate in climates:
        for ens_name, ens in ensembles.items():
            if climate in ens_name:
                ensembles[ens_name]['data_initial'] = ensembles[f"{climate}-initial"]['data'].copy()
                ens['climate'] = climate

    for i,experiment_identifier in enumerate([f"x{i}" for i in range(1,7)]):
        ens = ensembles[f'ssp370-2025-{experiment_identifier}']
        ens['color'] = sns.cubehelix_palette(6, start=3, rot=0.2, dark=.2, light=.8, reverse=True)[i-1]
        ens['marker'] = (2, 0 ,30*i)
        ens['linestyle'] = ':' 
        ens['long_name'] = f"{ens['climate']} rea{i}"   
    
    for i,experiment_identifier in enumerate([f"x{i}" for i in range(1,7)]):
        ens = ensembles[f'piControl-{experiment_identifier}']
        ens['color'] = sns.cubehelix_palette(6, start=2, rot=0.2, dark=.2, light=.8, reverse=True)[i-1]
        ens['marker'] = (2, 0 ,30*i)
        ens['linestyle'] = ':'
        ens['long_name'] = f"{ens['climate']} rea{i}"   

    for ens_name, ens in ensembles.items():
        if 'x' not in ens_name:
            if 'piControl' in ens_name:
                ens['color'] = 'c'
                ens['linestyle'] = '-'
                ens['marker'] = (2, 0 ,30)
            else:
                ens['color'] = 'm'
                ens['linestyle'] = '-'
                ens['marker'] = (2, 0 ,30)

        if 'wet' in ens_name:
            ens['color'] = 'b'
            ens['linestyle'] = ':'
            ens['marker'] = (2, 0 ,30*8) 
        if 'dry' in ens_name:
            ens['color'] = 'orange'
            ens['marker'] = (2, 0 ,30*8)
            ens['linestyle'] = ':'
      




    for ens_name,ens in ensembles.items():
        if 'initial' in ens_name:
            possible_vars = list(ens['data'].keys())
            for var in possible_vars:
                if f"{var}-before" in ens['data'].keys():
                    ens['data'][f"{var}-all"] = xr.concat((ens['data'][f"{var}-before"], ens['data'][f"{var}"]), dim='time')

    for ens_name,ens in ensembles.items():
        if 'initial' not in ens_name:
            possible_vars = list(ens['data'].keys())
            for var in possible_vars:
                if f"{var}-before" in ens['data_initial'].keys():
                    before = ens['data_initial'][f"{var}-before"]
                    l = []
                    for sim_name in ens['data'][f"{var}"].sim.values:
                        sim_number = int(str(sim_name)[3:6])
                        merged = xr.concat((
                            before[[sim_number]].assign_coords(sim=[sim_name]), 
                            ens['data'][f"{var}"].loc[[sim_name]]
                            ), dim='time')
                        l.append(merged)
                    ens['data'][f"{var}-all"] = xr.concat(l, dim='sim')

    for ens_name,ens in ensembles.items():
        for var in ens['data'].keys():
            if len(ens['data'][var].shape) > 1:
                if isinstance(ens['data'][var].time.values[0], np.int64) == False:
                    ens['data'][var] = ens['data'][var].assign_coords(time = [datetime.datetime.strptime(str(t)[:10], "%Y-%m-%d") for t in ens['data'][var].time.values])

    #for ens_name,ens in ensembles.items():
    #    ens['data']['tas-all'].values[ens['data']['tas-all'] > 270] -= 273.15

    return ensembles

