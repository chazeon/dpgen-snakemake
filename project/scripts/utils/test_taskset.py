import pytest
from taskset import *

@pytest.mark.parametrize('d, res', [
    (
	    {"a": [1, 2, 3], "b": [4, 5, 6]},
        [
            {'a': 1, 'b': 4}, {'a': 1, 'b': 5}, {'a': 1, 'b': 6},
            {'a': 2, 'b': 4}, {'a': 2, 'b': 5}, {'a': 2, 'b': 6},
            {'a': 3, 'b': 4}, {'a': 3, 'b': 5}, {'a': 3, 'b': 6},
        ]
    )

])
def test_iter_value_set_result(d, res):
    assert list(iter_value_set(d)) == res
    for _d in iter_value_set(d):
        assert d.keys() == _d.keys()
