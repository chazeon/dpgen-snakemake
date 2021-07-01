import sys
from collections import defaultdict

import click
import numpy as np
import ase.io
import ase.build

ofmt_kwargs = defaultdict(dict)
ofmt_kwargs["vasp"] = {
    "direct": True,
    "vasp5": True
}


# def sort_ase_atoms(atoms, tags=None):

#     if tags is None:
#         tags = set(atoms.get_chemical_symbols())

#     grouped = groupby(
#         sorted(enumerate(atoms), key=lambda x: x[1].symbol),
#         key=lambda x: str(x[1].symbol))

#     grouped = dict([(k, list(g)) for k, g in grouped])
#     indices = [idx for tag in tags for idx, atom in grouped[tag]]

#     if len(indices) != len(atoms):
#         raise RuntimeError("Missing / duplicate tags.")

#     return atoms[indices]

def sort_ase_atoms(atoms, tags=None):

    tags = tags if tags else []
    ntag = len(tags)
    tmaps = dict(zip(tags, enumerate(tags)))

    deco = sorted(
        enumerate(atoms),
        key=lambda item: tmaps.get(item[1].symbol, (ntag, item[1].symbol))
    )
    indices = [idx for idx, atom in deco]
    return atoms[indices]



@click.command()
# @click.argument("fname")
@click.option("-n", nargs=3, type=(int, int, int), default=[1,1,1])
@click.option("-t", "--tags", default=None)
@click.option("--ifmt", default="vasp", type=click.Choice(ase.io.formats.ioformats))
@click.option("--ofmt", default="vasp", type=click.Choice(ase.io.formats.ioformats))
def main(n, tags, ifmt, ofmt):

    # if fname == "-": fname = sys.stdin
    atoms = ase.io.read(sys.stdin, format=ifmt)
    atoms = ase.build.make_supercell(atoms, np.diag(n))
    if tags != None: tags = tags.split(",")
    atoms = sort_ase_atoms(atoms, tags=tags)
    ase.io.write(sys.stdout, atoms, format=ofmt, **ofmt_kwargs[ofmt])

if __name__ == "__main__":
    main()