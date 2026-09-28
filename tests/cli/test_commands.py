import json

import pytest
from typer.testing import CliRunner

from jotter.cli.app import app

runner = CliRunner()


@pytest.fixture(autouse=True)
def setup_env(temp_db_path):
    pass


def test_cli_add_and_list():
    res = runner.invoke(app, ["add", "my note", "-t", "work"])
    assert res.exit_code == 0
    assert "Added #1" in res.stdout

    res = runner.invoke(app, ["list"])
    assert res.exit_code == 0
    assert "my note" in res.stdout
    assert "work" in res.stdout


def test_cli_done_and_purge():
    runner.invoke(app, ["add", "task to close"])
    res = runner.invoke(app, ["done", "1"])
    assert res.exit_code == 0

    res = runner.invoke(app, ["purge"])
    assert res.exit_code == 0
    assert "Removed 1 closed note" in res.stdout


def test_cli_json_output():
    runner.invoke(app, ["add", "json task"])
    res = runner.invoke(app, ["show", "1", "--json"])
    assert res.exit_code == 0
    data = json.loads(res.stdout)
    assert data[0]["body"] == "json task"
