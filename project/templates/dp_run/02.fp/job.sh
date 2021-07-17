#!/bin/bash 
#SBATCH -J vm5                           
#SBATCH -o %j.out                    
#SBATCH -e %j.err 
#SBATCH -n 64
#SBATCH -N 1
#SBATCH -p shared
#SBATCH -t 02:00:00                      
#SBATCH -A col146

module purge
module load slurm
module load cpu/0.15.4  gcc/9.2.0  openmpi/3.1.6
module load fftw/3.3.8 openblas/0.3.10-openmp netlib-scalapack/2.1.0-openblas
module load sdsc

export PATH=/home/chazeon/SCRATCH/vasp/vasp.6.2.0-gnu-omp-openblas/bin:$PATH

export OMP_NUM_THREADS=1
export OMPI_MCA_btl="openib,self,vader"
export OMPI_MCA_btl_openib_if_include="mlx5_2:1"

PREFIX=vasp

[ ! -f $PREFIX.done ] && ibrun vasp_std 1>$PREFIX.out 2>$PREFIX.err
[ $? -eq 0 ] && touch $PREFIX.done