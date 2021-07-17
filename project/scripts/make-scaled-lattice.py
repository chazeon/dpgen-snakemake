import sys
from collections import defaultdict

import click
import numpy
import ase.io
import ase.build

ofmt_kwargs = defaultdict(dict)
ofmt_kwargs["vasp"] = {
    "direct": True,
    "vasp5": True
}

@click.command()
@click.option("-x", "-X", "--scale-by", type=click.FLOAT)
@click.option("-v", "-V", "--scale-to", type=click.FLOAT)
@click.option("--ifmt", default="vasp", type=click.Choice(ase.io.formats.ioformats))
@click.option("--ofmt", default="vasp", type=click.Choice(ase.io.formats.ioformats))
def main(scale_to, scale_by, ifmt, ofmt):
    atoms = ase.io.read(sys.stdin, format=ifmt)
    cell = atoms.cell
    if scale_to:
        factor = (scale_to / numpy.linalg.det(cell[:])) ** (1/3)
    elif scale_by:
        factor = scale_by
    else:
        factor = 1.0

    atoms.cell[:] *= factor
    pos = atoms.get_positions()
    atoms.set_positions(pos * factor)

    ase.io.write(sys.stdout, atoms, format=ofmt, **ofmt_kwargs[ofmt])

if __name__ == "__main__":
    main()