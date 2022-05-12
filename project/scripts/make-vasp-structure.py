import click
import dpdata
import sys

IFMT_CHOICES=["auto", *dpdata.format.Format().get_formats()]
OFMT_CHOICES=dpdata.format.Format().get_formats()

@click.command()
@click.argument("fin")
@click.argument("fout")
@click.option("-t", "--type-map")
@click.option("--ifmt", default="dump", type=click.Choice(IFMT_CHOICES), help="Input format.")
@click.option("--ofmt", default="vasp/poscar", type=click.Choice(OFMT_CHOICES), help="Output format.")
def main(fin, fout, ifmt, ofmt, type_map):
    if type_map: type_map = type_map.split(",")
    s=dpdata.System(fin, ifmt, type_map=type_map)
    s.to(ofmt, fout)


if __name__ == "__main__":
    main()