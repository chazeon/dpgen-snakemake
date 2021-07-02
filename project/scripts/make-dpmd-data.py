import click
import dpdata


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("-t", "--type-map", required=True)
@click.option("-o", "--outdir", required=True)
def main(files, type_map, outdir):

    type_map = type_map.split(",")
    labeled_system = dpdata.LabeledSystem()

    for ofile in files:
        s = dpdata.LabeledSystem(ofile, type_map=type_map)
        labeled_system.append(s)

    labeled_system.to_deepmd_raw(outdir)
    labeled_system.to_deepmd_npy(outdir)

if __name__ == "__main__":
    main()