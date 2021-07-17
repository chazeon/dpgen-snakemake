#!/bin/bash 
#SBATCH -J vm5                           
#SBATCH -o %j.out                    
#SBATCH -e %j.err 
#SBATCH -A col146
#SBATCH -p gpu-shared
#SBATCH -t 48:00:00
#SBATCH --nodes 1
#SBATCH --gpus 1
#SBATCH --ntasks-per-node 10
#SBATCH --mem 96G


module load sdsc
module load gpu
module load gcc openmpi

source /home/chazeon/SCRATCH/qe-jobs/20210706-AlOOH/project/env/machine/expanse/deepmd.env

date
CKPT=model.ckpt

if [ ! -f "${CKPT}.index" ]
then
    echo "Checkpoint ${CKPT} not exist, start from scratch."
    dp train params.yml
elif [ ! -f "lcurve.out" ]
then
    echo "Checkpoint ${CKPT} exist, but start lcurve does not, start from ${CKPT}."
    dp train params.yml --init-model $CKPT
else 
    echo "Checkpoint ${CKPT} exist and lcurve exist, restarting."
    dp train params.yml --restart $CKPT
fi

dp freeze -o graph.pb