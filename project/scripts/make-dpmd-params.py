import sys

import click
import yaml
import numpy


RANDOM_MAX = sys.maxsize


@click.command(help="Generate new params from FIN.")
@click.argument("fin", type=click.Path(exists=True))
@click.option("-s", "--system", multiple=True)
def main(fin, system):

    with open(fin) as fp:
        params = yaml.safe_load(fp)

    params["model"]["descriptor"]["seed"] =  numpy.random.randint(RANDOM_MAX)
    params["model"]["fitting_net"]["seed"] = numpy.random.randint(RANDOM_MAX)
    params["training"]["seed"] =             numpy.random.randint(RANDOM_MAX)

    params["training"]["systems"].extend(system)
    
    yaml.dump(params, sys.stdout)
    

if __name__ == "__main__":
    main()