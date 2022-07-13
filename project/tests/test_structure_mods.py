from turtle import back
import numpy
import pytest
import importlib  
import sys
from pathlib import Path
import click.testing

TESTS_DIR = Path(__file__).parent

sys.path.insert(0, str(TESTS_DIR.parent / "scripts"))

inputs = [
    str(f) for f in 
    (TESTS_DIR / "data/POSCAR").glob("*")
]

assert len(inputs) > 0

@pytest.mark.parametrize("input_file", inputs)
def test_make_scaled_lattice_can_run(
    cli_runner: click.testing.CliRunner,
    input_file: str):

    main = importlib.import_module("make-scaled-lattice").main

    input_text = Path(input_file).read_text()

    result: click.testing.Result = \
         cli_runner.invoke(main, [], input=input_text)

    assert result.exit_code == 0
    assert result.stderr_bytes == None
    assert result.stdout_bytes != None


@pytest.mark.parametrize("input_file", inputs)
def test_make_supercell_can_run(
    cli_runner: click.testing.CliRunner,
    input_file: str):

    main = importlib.import_module("make-supercell").main

    input_text = Path(input_file).read_text()

    result: click.testing.Result = \
         cli_runner.invoke(main, [], input=input_text)

    assert result.exit_code == 0
    assert result.stderr_bytes == None
    assert result.stdout_bytes != None


@pytest.mark.parametrize("input_file", inputs)
def test_sort_ase_atoms(input_file: str):

    import ase, ase.io 

    sort_ase_atoms = importlib.import_module("make-supercell").sort_ase_atoms
    atoms = ase.io.read(input_file, format="vasp")

    for _ in range(3):

        # Test multiple times to avoid shuffling confliction

        symbols = numpy.unique(atoms.get_chemical_symbols()).tolist()
        numpy.random.shuffle(symbols)

        new_atoms = sort_ase_atoms(atoms, tags=symbols) # type: ase.Atoms
        new_symbols = new_atoms.get_chemical_symbols()

        tmp = [symbols.index(t) for t in new_symbols]

        # Assume in increasing order
        assert numpy.all(numpy.diff(tmp) >= 0)

        if len(symbols) > 1:
            # Assume is not all zero 
            assert numpy.any(numpy.diff(tmp) > 0)


@pytest.mark.parametrize("input_file", inputs)
def test_remap_ase_atomic_numbers(input_file: str):

    import ase, ase.io 

    remap_ase_atomic_numbers = importlib.import_module("make-supercell").remap_ase_atomic_numbers
    atoms = ase.io.read(input_file, format="vasp")

    symbols = numpy.unique(atoms.get_chemical_symbols()).tolist()
    numpy.random.shuffle(symbols)

    n0 = atoms.numbers
    n1 = remap_ase_atomic_numbers(n0, tags=symbols)
    n2 = remap_ase_atomic_numbers(n1, tags=symbols, back=True)
    n3 = remap_ase_atomic_numbers(n2, tags=symbols)

    numpy.testing.assert_array_equal(n0, n2)
    numpy.testing.assert_array_equal(n1, n3)

    assert numpy.all(n1 >= 1)
    assert numpy.all(n1 <= len(symbols))
    assert len(numpy.unique(n1).tolist()) == len(symbols)

