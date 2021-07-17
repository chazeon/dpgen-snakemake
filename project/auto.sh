set +x
shopt -s globstar

USER=$(whoami)
CWD=$(pwd -P)

ITER=$1

echo "Dispatching iter.$ITER."
sleep 10

# Wailt for folder

while true
do
    [ -d $CWD/dp_run/iter.$ITER/00.train ] && break
    sleep 1m
done

# # Train ...

snakemake -j8 dp_run_train_target

cd $CWD/dp_run/iter.$ITER/00.train
for i in {000..003}
do
    cd $i
    sbatch job.sh
    cd ..
done

cd $CWD

# Wait for training

while true
do
    [ "$(squeue -h -u $USER | grep 'vm5' | wc -l)" == "0" ] && break
    sleep 1m
done

snakemake -j1 dp_run_freeze_target

# Model_devi ...

snakemake -j20 dp_run_model_devi_target

cp $CWD/templates/dp_run/01.model_devi/job-bundle.sh \
   $CWD/dp_run/iter.$ITER/01.model_devi/job-bundle.sh

cd $CWD/dp_run/iter.$ITER/01.model_devi/
sbatch job-bundle.sh

cd $CWD

# Wait for model_devi

while true
do
    python3 scripts/plot-devi.py dp_run/iter.$ITER/01.model_devi/**/model_devi.out --x-lim 0 500 -o model_devi.iter.$ITER.png
    [ "$(squeue -h -u $USER | grep 'vm5' | wc -l)" == "0" ] && break
    sleep 1m
done

# Fp ...

snakemake -j20 dp_run_fp_target

cp $CWD/templates/dp_run/02.fp/job-bundle.sh $CWD/dp_run/iter.$ITER/02.fp/

cd $CWD/dp_run/iter.$ITER/02.fp/
sbatch job-bundle.sh
cd $CWD


for f in `find | grep job.sh`
do
    cd $(dirname $f) ;
    sbatch job.sh
    cd ..
    sleep 3
done 

while true
do
    [ "$(squeue -h -u $USER | grep 'vm5' | wc -l)" == "0" ] && sbatch job-bundle.sh
    sleep 1m
done

cd $CWD

# Wait for fp

while true
do
    [ "$(squeue -h -u $USER | grep 'vm5' | wc -l)" == "0" ] && break
    sleep 1m
done

snakemake -j8 dp_run_fp_collect