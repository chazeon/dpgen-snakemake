
import click
import dpdata


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("-t", "--type-map", required=True)
@click.option("-o", "--outdir", required=True)
def main(files, type_map, outdir):

    type_map = type_map.split(",")
    msys = dpdata.MultiSystems()
    for ofile in files:
        s = dpdata.LabeledSystem(ofile, type_map=type_map)
        msys.append(s)
    
    msys.to_deepmd_raw(outdir)
    msys.to_deepmd_npy(outdir)

if __name__ == "__main__":
    main()