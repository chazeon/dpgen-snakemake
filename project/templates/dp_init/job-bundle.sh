#!/bin/bash 
#SBATCH -J vmd                           
#SBATCH -o %j.out                    
#SBATCH -e %j.err 
#SBATCH -n 68 # 68 per core                           
#SBATCH -N 2
#SBATCH -p normal
#SBATCH -t 48:00:00                      


JOBFILE="job.sh"
CWD=$(pwd -P)

for j in $(find | grep ${JOBFILE})
do
    cd $(dirname $j)
    pwd -P
    bash $JOBFILE
    cd ${CWD}
done
