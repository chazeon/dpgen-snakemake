import click
import ase.io
from deepmd.calculator import DP
import numpy
from pathlib import Path
import pandas

import uuid
from deepmd.freeze import freeze_graph

from tqdm import tqdm

@click.command(help="Calculate the energy and force of the structure")
@click.argument("files", nargs=-1)
# @click.argument("graphs", nargs=-1)
@click.option("--num-graphs", default=4, type=click.INT)
@click.option("--fmt", type=click.Choice(ase.io.formats.ioformats), default="vasp")
@click.option("-o", "--output", default=None)
def main(files, num_graphs, fmt, output, **kwargs):

    structures = files[:-num_graphs]
    graphs = list(files[-num_graphs:])

    ns = len(structures)
    ng = len(graphs)

    df = pandas.DataFrame()

    
    for i in range(len(graphs)):

        g = graphs[i]

        if Path(g).is_dir():
            name = f"graph.tmp.pb"
            freeze_graph(g, name)

            graphs[i] = f"{g}/{name}"


    for fname in tqdm(structures):

        s = ase.io.read(fname, format=fmt)
        na = s.get_number_of_atoms()

        energies = numpy.zeros((ng,))
        forces = numpy.zeros((ng, na, 3))

        for g in graphs:

            s.calc = DP(model=g)
            energies[i] = s.get_potential_energy()
            forces[i,:] = s.get_forces()

        df.loc[fname,["e_devi", "f_devi(x)", "f_devi(y)", "f_devi(z)"]] = ([
            numpy.std(energies),
            *numpy.average(numpy.std(forces, axis=0), axis=0)
        ])

        print(df.loc[fname])

        if output:
            with open(output, "w") as fp:
                fp.write(df.to_string())

if __name__ == "__main__":
    main()