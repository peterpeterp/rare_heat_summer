class configuration_parameters():
    def __init__(self):
        self.version=215
        self.res = 'f09_g17'
        self.mach = 'levante'
        self.compiler = 'intel'
        self.mpilib = 'openmpi'
        self.queue = 'default'
        self.walltime = '12:00:00'
        self.ntasks = 512
        self.ntasks_wav = 16

conf = configuration_parameters()

# specify these directories
dir_scripts=f'PATH_TO_SPECIFY'
dir_run=f'PATH_TO_SPECIFY'
dir_repo=f'PATH_TO_SPECIFY'
dir_user_nl = f'PATH_TO_SPECIFY'


sbatch_modules = '''
module purge
module load subversion python3/2022.01-gcc-11.2.0 esmf/8.2.0-intel-2021.5.0
module load esmf/8.2.0-intel-2021.5.0 gcc intel-oneapi-compilers/2022.0.1-gcc-11.2.0 intel-oneapi-mkl/2022.0.1-gcc-11.2.0
module load openmpi/4.1.2-intel-2021.5.0
module load cdo nco python3/2022.01-gcc-11.2.0
module load nano emacs ncview tree
'''

sbatch_job_header = '''#!/bin/bash\n
#SBATCH --partition=compute     # Specify partition name
#SBATCH --ntasks=1             # Specify max. number of tasks to be invoked
#SBATCH --cpus-per-task=1     # Specify number of CPUs per task
#SBATCH --time=04:00:00        # Set a limit on the total run time
#SBATCH --output=log/%j    # File name for standard output
#SBATCH --error=log/%j    # File name for standard error output
'''