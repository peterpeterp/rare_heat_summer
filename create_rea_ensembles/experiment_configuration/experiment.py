import sys,os,glob,importlib
import numpy as np
from experiment_configuration.main_observable import main_observable

class experiment():
    def __init__(self, config, online=True):
        # general settings
        self.dkrz_project_for_archive = 'bb1152'
        self.dkrz_project_for_accounting = 'bb1445'
        self.dir_scripts=f"/work/bb1152/u290372/cesm215/cime/scripts"
        self.dir_run=f"/scratch/u/u290372/cesm215_output"
        self.dir_work=f"/work/bb1152/u290372"

        # launching script
        self.launching_script = "/home/u/u290372/projects/REA_with_CESM2/branch_perturbed.py"

        # perturbation method and order of magnitude
        self.perturbation_order_of_magnitude = -13
        self.perturbation_type = 'PT_direct'

        # experiment name
        self.product_name = "heat_wEU_JJA"

        # git repo
        self.git_repo = "https://github.com/peterpeterp/REA_heat_wEU_JJA"

        # length of simulation steps
        self.n_days = 5

        # number of steps
        self.n_steps = 18

        # observable of interest
        self.observable_of_interest = 'TREFHT'

        # region of interest
        self.region_of_interest = 'wEU'

        # CESM2 output to save
        self.output = 'gklt_summer'

        # add variables from specific configuration
        for k,v in config.__dict__.items():
            self.__dict__[k] = v

        # start date in year
        self.start_date_in_year = '05-31'

        ini_config_module = importlib.import_module(f"experiment_configuration.initial_conditions.{self.initial_conditions_name}")
        ini_config = ini_config_module.initial_condition_config(self.start_date_in_year)
        for k,v in ini_config.__dict__.items():
            self.__dict__[k] = v        

        if online:
            if 'dry' in self.experiment_identifier or 'wet' in self.experiment_identifier:
                assert self.n_members == 100, \
                    f"the number of initial conditions has changed: expected=100 got={self.n_members}" 
            else:               
                assert self.n_members == 42*3, \
                    f"the number of initial conditions has changed: expected=42*3 got={self.n_members}"
        else:
            if 'dry' in self.experiment_identifier or 'wet' in self.experiment_identifier:
                self.n_members = 100
            else:               
                self.n_members = 42*3
                
        # experiment name
        self.experiment_name = f"{self.region_of_interest}.{self.observable_of_interest}.{self.start_date_in_year}.{self.n_days}x{self.n_steps}.{self.initial_conditions_name}.k{str(self.k).replace('.','p')}.s{self.seed}"

        self.experiment_new_identifier = ''.join(self.experiment_identifier.split('_')[0][1:])

        # python environment required for the computation of main_observable
        self.python_environment_path = '/home/u/u290372/.conda/envs/py_imps/bin/python'

        # template dict for todos
        # the dict will later be transformed to command line arguments for the launching script
        self.launch_template = {
            "dkrz_project_for_archive" : self.dkrz_project_for_archive,
            "case_identifier" : "",
            "case_path" : "",
            "parent_path" : "",
            "precompiled_path" : "",
            "perturbation_seed" : "",
            "compset" : self.compset,
            "ndays" : self.n_days,
            "perturbation_type" : self.perturbation_type,
            "perturbation_order_of_magnitude" : self.perturbation_order_of_magnitude,
            "user_nl_file_directory" : '/home/u/u290372/projects/REA_heat_wEU_JJA/experiment_configuration/user_nl_files',
        }

        self.dir_archive=f"/work/{self.dkrz_project_for_archive}/u290372/cesm215_archive"
        self.dir_out = f"{self.dir_work}/GKLT/{self.experiment_name}"
        self.dir_archive_post = f"{self.dir_archive}/GKLT/{self.experiment_name}"

    def get_main_observable(self, archive_path):
        return float(main_observable(archive_path))

    def calc_score(self, x):
        return float(np.exp(self.k * x))




