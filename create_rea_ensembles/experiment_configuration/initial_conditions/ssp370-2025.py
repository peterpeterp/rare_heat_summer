import sys,os,glob

class initial_condition_config():
    def __init__(self, start_date_in_year):
        self.start_date_in_year = start_date_in_year

        # compset
        self.compset = "BSSP370cmip6"

        # initial condition restart files
        self.initial_condition_fake_year = 2025
        self.initial_conditions = sorted(glob.glob(f"/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.*.fE.2020.ens000/*-01-01_to_*-{start_date_in_year}"))

        # number of members
        self.n_members = len(self.initial_conditions)

