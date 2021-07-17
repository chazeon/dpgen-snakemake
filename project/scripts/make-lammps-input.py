import click
import jinja2
import yaml
import random
import sys
import itertools

RAND_MAX = 2 ** 16

@click.command()
@click.argument("template", type=click.Path(exists=True))
@click.argument("params", type=click.Path(exists=True))
def main(template, params):

    with open(params) as fp:
        params = yaml.safe_load(fp)

    with open(template) as fp:
        t = jinja2.Template(fp.read(), keep_trailing_newline=True)

    params["seed"] = random.randint(0, RAND_MAX)

    sys.stdout.write(t.render(**params))


if __name__ == "__main__":
    main()