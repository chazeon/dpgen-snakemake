#!/bin/bash 
#SBATCH -J vmd                           
#SBATCH -o %j.out                    
#SBATCH -e %j.err 
#SBATCH -n 68
#SBATCH -N 2
#SBATCH -p development
#SBATCH -t 02:00:00                      


module load intel/19.1.1

export PATH=/home1/05774/tg850736/WORK2/20210519-VASP/vasp6.2.0-knl/vasp.6.2.0/bin:$PATH
export OMP_NUM_THREADS=2

ibrun vasp_std 1>vasp.out 2>vasp.err
