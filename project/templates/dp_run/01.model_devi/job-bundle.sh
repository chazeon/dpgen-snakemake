#!/bin/bash 
#SBATCH -J vm5                           
#SBATCH -o %j.out                    
#SBATCH -e %j.err 
#SBATCH -A col146
#SBATCH -p gpu-shared
#SBATCH -t 24:00:00
#SBATCH --nodes 1
#SBATCH --gpus 1
#SBATCH --mem 96G
#SBATCH --ntasks-per-node 10


JOBFILE="job.sh"
CWD=$(pwd -P)

for j in $(find | grep ${JOBFILE})
do
    cd $(dirname $j)
    pwd -P
    bash $JOBFILE
    cd ${CWD}
done
