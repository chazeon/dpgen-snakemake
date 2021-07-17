import itertools

def iter_value_set(d: dict):
    for vs in itertools.product(*d.values()):
        yield dict(zip(d.keys(), vs))