import click
import pandas
from matplotlib import pyplot as plt

from pathlib import Path
from tqdm import tqdm

@click.command()
@click.argument("fdevi", nargs=-1)
@click.option("-o", "--output", default="model_devi.png")
@click.option("--x-lim", type=click.FLOAT, nargs=2)
def main(fdevi, output, x_lim):


    fig, axes = plt.subplots(2, 1, figsize=(4,6))

    for fname in tqdm(fdevi):

        df = pandas.read_fwf(fname, widths=[12] + [19] * 6, index_col=0)

        axes[0].plot(df.index, df["max_devi_f"], label=Path(fname).parts[-2])
        axes[1].plot(df.index, df["max_devi_e"], label=Path(fname).parts[-2])


    for ax in axes:
        ax.semilogy()
        if x_lim: ax.set_xlim(x_lim)
    
    # fig.legend(fontsize="small")


    plt.tight_layout()
    plt.savefig(output, dpi=144)


if __name__ == "__main__":
    main()