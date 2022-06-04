#!/bin/bash
#SBATCH -N 1
#SBATCH -p RM-shared
#SBATCH --ntasks-per-node=64
#SBATCH -t 48:00:00

ulimit -s unlimited
module load intelmpi
export OMP_NUM_THREADS=2
echo "SLURM_NTASKS: " $SLURM_NTASKS

export PATH=/opt/packages/VASP/VASP6/6.3/INTEL:$PATH

mpirun -np $SLURM_NTASKS vasp_std 1> vasp.out 2> vasp.err

rm CHG
rm CHGCAR
rm DOSCAR
rm EIGENVAL
rm WAVECAR
