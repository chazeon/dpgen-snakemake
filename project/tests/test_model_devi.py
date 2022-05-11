import pytest
import importlib  
import sys
from pathlib import Path
import click.testing

TESTS_DIR = Path(__file__).parent

sys.path.insert(0, str(TESTS_DIR.parent / "scripts"))

inputs = [
    (
        str(TESTS_DIR / "data/model_devi.out"),
        (0.02, 0.05),
        str(TESTS_DIR / "data/traj"),
    )
]

@pytest.mark.parametrize("fdevi, f_limit, traj", inputs)
def test_filter_devi(
    cli_runner: click.testing.CliRunner,
    tmp_path: Path,
    fdevi: str, f_limit: tuple, traj: str):

    main = importlib.import_module("filter-devi").main
    fname = str(tmp_path / "output.txt")

    result: click.testing.Result = \
         cli_runner.invoke(main, [fdevi, "--f-limit", *f_limit, "--traj", traj, "-o", fname])

    assert result.exit_code == 0
    assert result.stderr_bytes == None
    
    with open(fname) as fp:
        lines = fp.readlines()
        assert len(lines) > 1
        assert all([line.strip().endswith(".lammpstrj") for line in lines])