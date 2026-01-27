import sys,os,glob

class initial_condition_config():
    def __init__(self, start_date_in_year):
        self.start_date_in_year = start_date_in_year

        # compset
        self.compset = "BSSP370cmip6"

        # initial condition restart files
        self.initial_condition_fake_year = 2025

        self.initial_conditions = []

        wet_selection = [
            '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.1300.fE.2020.ens000/2024-01-01_to_2024-05-31',
            '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens022.fE.2020.ens000/2025-01-01_to_2025-05-31',
            '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens009.fE.2020.ens000/2026-01-01_to_2026-05-31',
            '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens020.fE.2020.ens000/2025-01-01_to_2025-05-31',
            '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens012.fE.2020.ens000/2025-01-01_to_2025-05-31',
            '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens008.fE.2020.ens000/2024-01-01_to_2024-05-31',
            '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens013.fE.2020.ens000/2025-01-01_to_2025-05-31',
            '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens001.fE.2020.ens000/2025-01-01_to_2025-05-31',
            '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens024.fE.2020.ens000/2025-01-01_to_2025-05-31',
            '/work/bb1445/u290372/cesm215_archive/BSSP370cmip6_current_2021-2031/b.e215.BSSP370cmip6.f09_g17.001.2005.ens005.fE.2020.ens000/2025-01-01_to_2025-05-31'
        ]

        for sim in wet_selection:
            for i in range(10):
                self.initial_conditions.append(sim)

        # number of members
        self.n_members = len(self.initial_conditions)

