import sys
from collections import defaultdict

import numpy
import click
import ase.io
import ase.build
from ase.symbols import symbols2numbers

ofmt_kwargs = defaultdict(dict)
ofmt_kwargs["vasp"] = {
    "direct": True,
    "vasp5": True
}


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

def remap_ase_atomic_numbers(numbers: numpy.array, tags: list):
    '''
    Given numbers and tags, remap to [1, 2, 3, ...]
    '''
    tmap = dict((v, k + 1) for k, v in enumerate(symbols2numbers(tags)))
    numbers = numpy.vectorize(lambda t: tmap[t])(numbers)
    return numbers


@click.command()
@click.option("-n", nargs=3, type=(int, int, int), default=[1,1,1])
@click.option("-t", "--tags", default=None)
@click.option("--remap", is_flag=True, default=False, help="Remap atomic numbers")
@click.option("--ifmt", default="vasp", type=click.Choice(ase.io.formats.ioformats))
@click.option("--ofmt", default="vasp", type=click.Choice(ase.io.formats.ioformats))
def main(n, tags, ifmt, ofmt, remap):
    atoms = ase.io.read(sys.stdin, format=ifmt)

    if tags != None: tags = tags.split(",")

    if remap and tags != None:
        numbers = atoms.get_atomic_numbers()
        numbers = remap_ase_atomic_numbers(numbers, tags)
        atoms.set_atomic_numbers(numbers)

    atoms = ase.build.make_supercell(atoms, numpy.diag(n))
    atoms = sort_ase_atoms(atoms, tags=tags)
    ase.io.write(sys.stdout, atoms, format=ofmt, **ofmt_kwargs[ofmt])

if __name__ == "__main__":
    main()
