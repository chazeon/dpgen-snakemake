#!/bin/bash 
#SBATCH -J vmd                           
#SBATCH -o %j.out                    
#SBATCH -e %j.err 
#SBATCH -n 68
#SBATCH -N 2
#SBATCH -p normal
#SBATCH -t 48:00:00                      

source /home1/05774/tg850736/WORK2/20210529-deepmd/20210628-dpgen-mphys/project/env/machine/stampede2/deepmd.env
dp train params.yml