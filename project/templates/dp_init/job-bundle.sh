#!/bin/bash 
#SBATCH -J vm6                           
#SBATCH -o %j.out                    
#SBATCH -e %j.err 
#SBATCH -n 64
#SBATCH -N 2
#SBATCH -p compute
#SBATCH -t 48:00:00                      
#SBATCH -A TG-DMR180081                 


JOBFILE="job.sh"
CWD=$(pwd -P)

for j in $(find | grep ${JOBFILE})
do
    cd $(dirname $j)
    pwd -P
    bash $JOBFILE
    cd ${CWD}
done
