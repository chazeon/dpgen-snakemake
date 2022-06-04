import pytest
import importlib  
import sys
from pathlib import Path
import click.testing

TESTS_DIR = Path(__file__).parent

sys.path.insert(0, str(TESTS_DIR.parent / "scripts"))

cases = [
    (
        "T = {{temp}}",
        ["temp=300"],
        "T = 300",
    ),
    (
        "{{condition}}",
        ["condition=temp=300"],
        "temp=300",
    )
]

@pytest.mark.parametrize("input_text, args, output_text", cases)
def test_renders(
    cli_runner: click.testing.CliRunner,
    input_text: str, args: list, output_text: str
):

    main = importlib.import_module("render-template").main

    result: click.testing.Result = \
         cli_runner.invoke(main, args, input=input_text)

    assert result.exit_code == 0
    assert result.stderr_bytes is None
    assert result.stdout_bytes is not None
    assert result.stdout == output_text
    

@pytest.mark.parametrize("input_text, args, output_text", cases)
def test_fails_on_missing_params(
    cli_runner: click.testing.CliRunner,
    input_text: str, args: list, output_text: str
):

    main = importlib.import_module("render-template").main

    result: click.testing.Result = \
         cli_runner.invoke(main, ["X=0"], input=input_text)

    assert result.exit_code != 0