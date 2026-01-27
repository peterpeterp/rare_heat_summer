#!/bin/bash
#SBATCH --job-name=sim_launcher      # Specify job name
#SBATCH --partition=compute     # Specify partition name
#SBATCH --ntasks=1             # Specify max. number of tasks to be invoked
#SBATCH --cpus-per-task=1     # Specify number of CPUs per task
#SBATCH --time=04:00:00        # Set a limit on the total run time
#SBATCH --account=uc1275       # Charge resources on this project account
#SBATCH --output=log/%j    # File name for standard output
#SBATCH --error=log/%j    # File name for standard error output
python ~/projects/cesm215_peters_scripts/branch.py --compset B1850cmip6 --parent b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000 --output minimal --precompiled b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000/branch/0501-01-01_to_0501-04-30 --startdate 0711-01-01 --enddate 0711-04-30 --overwrite
python ~/projects/cesm215_peters_scripts/branch.py --compset B1850cmip6 --parent b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000 --output minimal --precompiled b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000/branch/0501-01-01_to_0501-04-30 --startdate 0723-01-01 --enddate 0723-04-30 --overwrite
python ~/projects/cesm215_peters_scripts/branch.py --compset B1850cmip6 --parent b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000 --output minimal --precompiled b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000/branch/0501-01-01_to_0501-04-30 --startdate 0726-01-01 --enddate 0726-04-30 --overwrite
python ~/projects/cesm215_peters_scripts/branch.py --compset B1850cmip6 --parent b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000 --output minimal --precompiled b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000/branch/0501-01-01_to_0501-04-30 --startdate 0729-01-01 --enddate 0729-04-30 --overwrite
python ~/projects/cesm215_peters_scripts/branch.py --compset B1850cmip6 --parent b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000 --output minimal --precompiled b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000/branch/0501-01-01_to_0501-04-30 --startdate 0735-01-01 --enddate 0735-04-30 --overwrite
python ~/projects/cesm215_peters_scripts/branch.py --compset B1850cmip6 --parent b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000 --output minimal --precompiled b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000/branch/0501-01-01_to_0501-04-30 --startdate 0756-01-01 --enddate 0756-04-30 --overwrite
python ~/projects/cesm215_peters_scripts/branch.py --compset B1850cmip6 --parent b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000 --output minimal --precompiled b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000/branch/0501-01-01_to_0501-04-30 --startdate 0768-01-01 --enddate 0768-04-30 --overwrite
python ~/projects/cesm215_peters_scripts/branch.py --compset B1850cmip6 --parent b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000 --output minimal --precompiled b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000/branch/0501-01-01_to_0501-04-30 --startdate 0789-01-01 --enddate 0789-04-30 --overwrite
python ~/projects/cesm215_peters_scripts/branch.py --compset B1850cmip6 --parent b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000 --output minimal --precompiled b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000/branch/0501-01-01_to_0501-04-30 --startdate 0804-01-01 --enddate 0804-04-30 --overwrite
