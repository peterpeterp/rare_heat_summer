import sys,os,glob

class initial_condition_config():
    def __init__(self, start_date_in_year):
        self.start_date_in_year = start_date_in_year

        # compset
        self.compset = "BSSP370cmip6"

        # initial condition restart files
        self.initial_condition_fake_year = 2025

        self.initial_conditions = []

        dry_selection = ['/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens020.fE.2020.ens000/2024-01-01_to_2024-05-31',
       '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.1200.fE.2020.ens000/2024-01-01_to_2024-05-31',
       '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens009.fE.2020.ens000/2025-01-01_to_2025-05-31',
       '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens016.fE.2020.ens000/2024-01-01_to_2024-05-31',
       '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens018.fE.2020.ens000/2025-01-01_to_2025-05-31',
       '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.1400.fE.2020.ens000/2024-01-01_to_2024-05-31',
       '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens011.fE.2020.ens000/2026-01-01_to_2026-05-31',
       '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens007.fE.2020.ens000/2026-01-01_to_2026-05-31',
       '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.1000.fE.2020.ens000/2024-01-01_to_2024-05-31',
       '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.0500.fE.2020.ens000/2024-01-01_to_2024-05-31']

        for sim in dry_selection:
            for i in range(10):
                self.initial_conditions.append(sim)




        # number of members
        self.n_members = len(self.initial_conditions)

