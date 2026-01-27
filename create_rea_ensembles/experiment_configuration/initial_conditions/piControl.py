import sys,os,glob

class initial_condition_config():
    def __init__(self, start_date_in_year):
        self.start_date_in_year = start_date_in_year

        # compset
        self.compset = "B1850cmip6"

        # initial condition restart files
        self.initial_condition_fake_year = 1850
        self.initial_conditions = sorted(glob.glob(f"/work/bb1445/u290372/cesm215_archive/b.e215.B1850cmip6.f09_g17.001.fE.0500.ens000/branch/*-01-01_to_*-04-30/branch/*-04-30_to_*-05-31"))

        # number of members
        self.n_members = len(self.initial_conditions)

