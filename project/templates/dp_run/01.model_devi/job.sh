#!/bin/bash 
#SBATCH -J vm5                           
#SBATCH -o %j.out                    
#SBATCH -e %j.err 
#SBATCH -A col146
#SBATCH -p gpu-debug
#SBATCH -t 00:30:00
#SBATCH --nodes 1
#SBATCH --gpus 1
#SBATCH --ntasks-per-node 10
#SBATCH --mem 96G

module load gpu

source /home/chazeon/SCRATCH/qe-jobs/20210715-AlOOH-m5/env/machine/expanse/deepmd.env

lmp -in input.lmp 1> lmp.out 2> lmp.err
if [ $? -eq 0 ]
then
    touch lmp.done
fi