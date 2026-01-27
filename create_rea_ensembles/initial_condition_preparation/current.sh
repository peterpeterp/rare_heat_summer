# commands like

for ens in 0400; do python ~/projects/cesm215_peters_scripts/branch.py --compset BSSP370cmip6 --parent b.e215.BSSP370cmip6.f09_g17.$ens.fE.2020.ens000  --startdate 2025-01-01 --enddate 2025-05-31 --precompiled b.e215.BSSP370cmip6.f09_g17.0400.fE.2020.ens000/2024-01-01_to_2024-05-31 --output minimal; done