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