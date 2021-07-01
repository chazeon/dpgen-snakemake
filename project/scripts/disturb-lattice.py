import sys
from io import StringIO
from collections import defaultdict

import click
import numpy as np
import ase.io
import ase.io.lammpsdata

ofmt_kwargs = defaultdict(dict)
ofmt_kwargs["vasp"] = {
    "direct": True,
    "vasp5": True
}


def random_range(a, b, ndata=1):
    data = np.random.random(ndata) * (b - a) + a
    return data

def gen_random_disturb(dmax, a, b, dstyle='uniform'):
    d0 = np.random.rand(3) * (b - a) + a
    dnorm = np.linalg.norm(d0)
    if dstyle == 'normal':
        dmax = np.random.standard_normal(0, 0.5) * dmax
    elif dstyle == 'constant':
        pass
    else:
        # use if we just wanna a disturb in a range of [0, dmax),
        dmax = np.random.random() * dmax
    dr = dmax / dnorm * d0
    return dr

def gen_random_emat(etmax, diag=0):
    if np.abs(etmax) >= 1e-6:
        e = random_range(-etmax, etmax, 6)
    else:
        e = np.zeros(6)
    if diag != 0:
        # isotropic behavior
        e[3], e[4], e[5] = 0, 0, 0
    emat = np.array(
        [[e[0], 0.5 * e[5], 0.5 * e[4]],
         [0.5 * e[5], e[1], 0.5 * e[3]],
         [0.5 * e[4], 0.5 * e[3], e[2]]]
    )
    emat = emat + np.eye(3)
    return emat


def create_disturbs(atoms, dmax=1.0, etmax=0.1, dstyle='uniform', write_d=False, diag=0):

    # read-in by ase
    natoms = atoms.get_number_of_atoms()
    cell0 = atoms.get_cell()

    # Use copy(), otherwise it will modify the input atoms every time.
    atoms_d = atoms.copy()

    # random flux for atomic positions
    dpos = np.zeros((natoms, 3))
    for i in range(natoms):
        dr = gen_random_disturb(dmax, -0.5, 0.5, dstyle)
        dpos[i, :] = dr

    # random flux for volumes
    cell = np.dot(cell0, gen_random_emat(etmax, diag))
    atoms_d.set_cell(cell, scale_atoms=True)
    
    # determine new cell & atomic positions randomiziations
    pos = atoms_d.get_positions() + dpos
    atoms_d.set_positions(pos)

    return atoms_d


@click.command()
@click.option("--d-cell", type=click.FLOAT)
@click.option("--d-atom", type=click.FLOAT)
@click.option("--ifmt", default="vasp", type=click.Choice(ase.io.formats.ioformats))
@click.option("--ofmt", default="vasp", type=click.Choice(ase.io.formats.ioformats))
def main(ifmt, ofmt, d_cell, d_atom):

    atoms = ase.io.read(sys.stdin, format=ifmt)
    atoms = create_disturbs(atoms, dmax=d_atom, etmax=d_cell)
    ase.io.write(sys.stdout, atoms, format=ofmt, **ofmt_kwargs[ofmt])

if __name__ == "__main__":
    main()