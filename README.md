# Scripts related to "Heat extremes within hot summer seasons intensify more than in average summers under global warming"

## First steps

### Install and test CESM2 (version 2.1.5)
Instructions and code can be found here: https://www.cesm.ucar.edu/models/cesm2

### Download relevant CESM2 large ensemble (LENS) data
Data description and download links can be found here: https://www.cesm.ucar.edu/community-projects/lens2

### Download the CMIP6 piControl run (optional)
CMIP6 data can be downloaded here: https://esgf-node.ipsl.upmc.fr/projects/cmip6-ipsl/

### Specify paths in scripts

Search for `PATH_TO_SPECIFY` in all scripts and replace with the location of your data or CESM2 installation.

## Run rare-event sampling experiments
All scripts related to the rare-event sampling workflow are found in `create_rea_ensembles\`.

Ensemble simulations are launched using commands like:

`python REA_launcher.py --experiment c1`

where `c1` is an experiment configuration specified in `experiment_configurations/c1.py`. The combination of  `experiment_configurations/experiment.py` and `experiment_configurations/c1.py` specify the full configuration.

## Main analysis

Run all cells in the following jupyter notebooks:

| jupyter notebook | purpose |
--------------|----------| 
| analysis/0_prepare_data_pickle.ipynb | Load regional averages and meta data or rare-event sampling ensembles |
| analysis/1_main_analysis.ipynb | Analysis using regional averages (most plots of the paper) |
| analysis/2_composite_maps.ipynb | All analysis with gridded data |

## Contact

Please don't hesitate to contact me if you have questions concerning the analysis.