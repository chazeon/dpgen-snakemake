'''
Render template from STDIN and write to STDOUT.
Template variables should be passed in as arguments like 'arg1=xxx arg2=xxx'.
'''

import click
import jinja2
import sys

env = jinja2.Environment(undefined=jinja2.StrictUndefined)

@click.command(help=__doc__)
@click.argument("args", nargs=-1, required=True)
def main(args):
    args = dict(pair.split("=", 1) for pair in args)
    template = env.from_string(sys.stdin.read())
    sys.stdout.write(template.render(**args))

if __name__ == "__main__":
    main()