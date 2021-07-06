import click
import dpdata
import sys

IFMT_CHOICES=["auto", *dpdata.System.register_from_funcs.funcs.keys()]
OFMT_CHOICES=dpdata.System.register_to_funcs.funcs.keys()

@click.command()
@click.argument("fin")
@click.argument("fout")
@click.option("--ifmt", default="auto", type=click.Choice(IFMT_CHOICES), help="Input format.")
@click.option("--ofmt", type=click.Choice(OFMT_CHOICES), help="Output format.")
def main(fin, fout, ifmt, ofmt):
    s=dpdata.System(fin, ifmt)
    s.to(ofmt, fout)


if __name__ == "__main__":
    main()