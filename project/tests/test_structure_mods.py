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
def test_sort_ase_atoms(
    input_file: str):

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

