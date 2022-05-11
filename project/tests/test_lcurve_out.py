import pytest
import importlib  
import sys
from pathlib import Path
import click.testing

TESTS_DIR = Path(__file__).parent

sys.path.insert(0, str(TESTS_DIR.parent / "scripts"))

inputs = [
    *(TESTS_DIR / "data/lcurve.out").glob("**/lcurve.out")
]

@pytest.mark.parametrize("ipath,", inputs)
def test_plot_lcurve(
    cli_runner: click.testing.CliRunner,
    tmp_path: Path,
    ipath: Path):

    main = importlib.import_module("plot-lcurve").main
    ofname = str(tmp_path / "lucrve.png")

    result: click.testing.Result = \
         cli_runner.invoke(main, [str(ipath), "-o", ofname])

    assert result.exit_code == 0
    assert result.stderr_bytes == None

    opath = Path(ofname)

    assert opath.exists()
    assert opath.stat().st_size > 0
    