import click
import dpdata
import sys


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("-t", "--type-map", required=True)
@click.option("-o", "--outdir", required=True)
def main(files, type_map, outdir):

    type_map = type_map.split(",")
    labeled_system = dpdata.LabeledSystem()

    for ofile in files:
        try:
            s = dpdata.LabeledSystem(ofile, type_map=type_map)
            labeled_system.append(s)
            print(ofile)
            print(len(s))
        except Exception as e:
            sys.stderr.write(f"{ofile} might be corrupted.\n")
            sys.stderr.write(str(e) + "\n")

    labeled_system.to_deepmd_raw(outdir)
    labeled_system.to_deepmd_npy(outdir)

if __name__ == "__main__":
    main()