import sh
from pathlib import Path
from matplotlib import pyplot as plt
import ase.io
import numpy
from functools import lru_cache
import pandas


@lru_cache()
def get_model_devi(fname):
    return pandas.read_fwf(fname, widths=[12] + [19] * 6, index_col=0)



with open("/home/chazeon/SCRATCH/qe-jobs/20210715-AlOOH-m5/dp_run/iter.000000/01.model_devi.candidate.shuffled.dat") as fp:
    trajs = fp.readlines()

for fname in Path("dp_run/iter.000000/02.fp").glob("**/OUTCAR"):

    try:
        etot = sh.tail(sh.grep("TOTEN", str(fname)), "-n1").stdout.decode()
        etot = float(etot.strip().split()[-2])
    except sh.ErrorReturnCode_1:
        continue

    i = int(fname.parts[-2])


    try:
        sh.grep("I HOPE YOU KNOW WHAT YOU ARE DOING!", str(fname)).stdout.decode().strip()
        flag = False
    except sh.ErrorReturnCode_1:
        flag = True

    n = int(Path(trajs[i].strip()).stem)

    dvf = get_model_devi(Path(trajs[i].strip()).parent / "../model_devi.out").loc[n, "max_devi_f"]
    dve = get_model_devi(Path(trajs[i].strip()).parent / "../model_devi.out").loc[n, "max_devi_e"]

    cell = ase.io.read(fname.parent / "POSCAR")

    c = cell.get_cell()
    # print(c)
    v = numpy.linalg.det(c)

    d = cell.get_all_distances(mic=True)
    dmin = numpy.min(d[d != 0])

    # plt.scatter(n, dmin / v ** (1/3), c=("r" if flag else "b"))
    plt.scatter(dvf, etot, c=("r" if flag else "b"))

    if flag: print(trajs[i].strip(), etot)

plt.savefig("etot.png", dpi=144)