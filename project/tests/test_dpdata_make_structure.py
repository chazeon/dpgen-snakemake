import pytest
import importlib  
import sys
from pathlib import Path
import click.testing
import ase.io.vasp, ase.io.lammpsdata
import re

TESTS_DIR = Path(__file__).parent

sys.path.insert(0, str(TESTS_DIR.parent / "scripts"))

inputs = [
    str(f) for f in 
    (TESTS_DIR / "data/POSCAR").glob("*")
]

assert len(inputs) > 0


def test_dpmd_formats():
    module = importlib.import_module("make-lammps-structure")
    assert len(module.IFMT_CHOICES) > 0
    assert len(module.OFMT_CHOICES) > 0

@pytest.mark.parametrize("input_file", inputs)
def test_make_scaled_lattice_can_run(
    cli_runner: click.testing.CliRunner,
    tmp_path: Path,
    input_file: str):

    main = importlib.import_module("make-lammps-structure").main

    # input_text = Path(input_file).read_text()
    output_file = str(tmp_path / "lmp.cfg")

    result: click.testing.Result = \
        cli_runner.invoke(main, [
            "--ifmt", "vasp/poscar",
            "--ofmt", "lammps/lmp",
            input_file,
            str(tmp_path / "lmp.cfg")
        ])

    assert result.exit_code == 0
    assert result.stderr_bytes == None

    input_structure = ase.io.vasp.read_vasp(file=input_file)
    output_text = Path(output_file).read_text()

    res = re.search(r"(\d+) atoms", output_text)
    assert int(res.group(1)) == len(input_structure.get_positions())
    
