from collections import defaultdict
import pandas
from matplotlib import colors, pyplot as plt
import click
from pathlib import Path
from copy import deepcopy
from io import StringIO


COLORS = plt.rcParams["axes.prop_cycle"].by_key()["color"]
KEYS = ["l2_tst", "l2_trn", "l2_e_tst", "l2_e_trn", "l2_f_tst", "l2_f_trn", "lr"]

@click.command()
@click.argument("lcurves", nargs=-1)
@click.option("--train/--no-train", default=True)
@click.option("--test/--no-test", default=True)
@click.option("-n", "--num-steps", default=None, type=click.INT)
@click.option("-o", "--output", type=click.Path(), help="Output file name.", default="lcurve.png")
def main(**kwargs):

    fig, axes = plt.subplots(2, 2, sharex=True)

    # colname = kwargs.pop("colname")
    lcurves = kwargs.pop("lcurves", [])
    colors = list(reversed(deepcopy(COLORS)))

    for fname in lcurves:
        label = Path(fname).parts[-2]
        color = colors.pop()

        with open(fname) as fp:
            lines = fp.readlines()
            lines = [line for idx, line in enumerate(lines) if idx == 0 or "batch" not in line]
        fp = StringIO("\n".join(lines))

        df = pandas.read_table(fp, sep=r"\s{2,}", header=0, index_col=0)
        for colname in KEYS:
            ax = {
                KEYS[0]: axes[0,0], KEYS[1]: axes[0,0],
                KEYS[2]: axes[0,1], KEYS[3]: axes[0,1],
                KEYS[4]: axes[1,0], KEYS[5]: axes[1,0],
                KEYS[6]: axes[1,1],
            }[colname]

            if kwargs.get("train") == False and colname.endswith("trn"): continue
            if kwargs.get("test") == False and colname.endswith("tst"): continue

            num_steps = kwargs.get("num_steps")
            if num_steps:
                df = df.loc[:num_steps]


            df.reset_index().plot.scatter(
                x="# batch", y=colname, ax=ax, label=label, color=color, marker=("x" if colname.endswith("tst") else "o"), alpha=.75)
            ax.semilogy()

            if colname != "lr":
                ax.get_legend().remove()
    
    plt.savefig(kwargs.get("output"), dpi=144)

if __name__ == "__main__":
    main()