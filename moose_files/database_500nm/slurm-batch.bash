#!/bin/bash

#SBATCH -J SAMPLE_JOB     # job name
#SBATCH -o log_slurm.o%j  # output and error file name (%j expands to jobID)
#SBATCH -n 8              # total number of tasks requested
#SBATCH -N 1              # cpus to allocate per task
#SBATCH -p bsudfq         # queue (partition) -- defq, eduq, gpuq, shortq
###SBATCH --exclusive
#####SBATCH --nodelist=r2-piret-01
#SBATCH -t 30-0:00:00       # run time (hh:mm:ss) - 12.0 hours in this example.
# Generally needed modules:
module load slurm
#module load intel/mkl
#module load intel/mpi
#module load moose-framework/moose-dev-gcc
module load moose-dev-gcc
#module load openmpi/gcc8/4.1.2
#module load cmake/gcc8/3.18.0
#module load valgrind/3.16.1
#module load petsc
## Example module loads for other software:
# module load vasp
# module load python/intel/3.5
# module load lammps
#module load tutor

export LIBRARY_PATH=/cm/shared/software/opt/linux-centos7-x86_64/gcc-9.2.0/libx11-1.7.0-u5s2reu2nx5vykhfimela2hmutk2vrg3/lib:${LIBRARY_PATH} 

# Execute the program:
mpiexec -n 8 ./idb4-opt -i FeCrCo.i --n-threads=16

## Some examples:
# mpirun vasp_std
# mpirun lmp_cpu -v x 32 -v y 32 -v z 32 -v t 100 < in.lj
# mpirun python3 script.py

# Exit if mpirun errored:
status=$?
if [ $status -ne 0 ]; then
    exit $status
fi
# Do some post processing.
