from os import sep
import click
import pandas
import sys
from pathlib import Path
from tqdm import tqdm

from io import StringIO

@click.command()
@click.argument("fdevi", nargs=-1)
@click.option("-f", "--f-limit", type=click.FLOAT, nargs=2, default=(1.50e-1, 3.50e-1))
@click.option("-e", "--e-limit", type=click.FLOAT, nargs=2, default=(0.00e+5, 1.00e+5))
@click.option("--traj", default="traj")
@click.option("--test-exists", default=False, is_flag=True)
@click.option("-o", "--output")
def main(fdevi, f_limit, e_limit, output, **kwargs):

    sio = StringIO()

    for fname in tqdm(fdevi):

        df = pandas.read_fwf(fname, widths=[12] + [19] * 6, index_col=0)
        fname = Path(fname)

        for idx, row in df[
            (df["max_devi_f"].between(min(f_limit), max(f_limit))) &
            (df["max_devi_e"].between(min(e_limit), max(e_limit)))
        ].iterrows():

            ftraj = fname.parent / kwargs.get("traj") / f"{idx}.lammpstrj"
            if not kwargs.get("test_exists") or ftraj.exists():
                sio.write(str(ftraj) + "\n")

    # sys.stdout.write(sio.read())
    fp = open(output, "w") if output else sys.stdout
    fp.write(sio.getvalue())
    if fp != sys.stdout: fp.close()


if __name__ == "__main__":
    main()