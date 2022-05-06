import click
import dpdata

DPDATA_FIELDS = [
    "cells", "coords", # dpdata.System
    "energies", "forces", "virials", "atom_pref" # dpdata.LabeledSystem
]

@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("-t", "--type-map", required=True, help="Type name of atoms as a comma seperated list.")
@click.option("-N", "--num-frames", type=click.INT, help="Number of random frames.")
@click.option("-o", "--outdir", required=True, help="Output dir.")
def main(files, type_map, num_frames=None, outdir=None):

    type_map = type_map.split(",")
    labeled_system = dpdata.LabeledSystem()

    for ofile in files:
        s = dpdata.LabeledSystem(ofile, type_map=type_map)
        labeled_system.append(s)

    if num_frames:
        labeled_system.shuffle()
        for k in DPDATA_FIELDS:
            if k in labeled_system.data:
                labeled_system.data[k] = labeled_system.data[k][:num_frames]
    
    labeled_system.to_deepmd_raw(outdir)
    labeled_system.to_deepmd_npy(outdir)

if __name__ == "__main__":
    main()
