import json
import sqlite3

import pytest
from typer.testing import CliRunner

from jotter.cli.app import app

runner = CliRunner()


@pytest.fixture
def clean_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("JOTTER_DB", str(db_path))
    return str(db_path)


def test_add_commands(clean_db):
    # Add success
    res = runner.invoke(app, ["add", "New note"])
    assert res.exit_code == 0
    assert "Added" in res.stdout

    # Empty state add
    res2 = runner.invoke(app, ["add", "   "])
    assert res2.exit_code != 0


def test_edit_command(clean_db):
    runner.invoke(app, ["add", "Initial Note"])

    # 1. Edit existing note
    res = runner.invoke(app, ["edit", "1", "--body", "Edited Note"])
    assert res.exit_code == 0

    # 2. Edit nonexistent note
    res = runner.invoke(app, ["edit", "99", "--body", "Ghost Note"])
    assert res.exit_code != 0

    # 3. Edit with empty body / whitespace
    res = runner.invoke(app, ["edit", "1", "--body", "   "])
    assert res.exit_code != 0

    # 4. Edit with Unicode
    runner.invoke(app, ["edit", "1", "--body", "Café 🚀"])

    # 5. Edit repeatedly
    runner.invoke(app, ["edit", "1", "--body", "Repeat 1"])
    runner.invoke(app, ["edit", "1", "--body", "Repeat 2"])

    # Verify in DB
    conn = sqlite3.connect(clean_db)
    cur = conn.cursor()
    cur.execute("SELECT body FROM notes WHERE id=1")
    val = cur.fetchone()[0]
    assert val == "Repeat 2"
    conn.close()


def test_state_machine(clean_db):
    runner.invoke(app, ["add", "State Note"])

    # done -> open -> done
    res1 = runner.invoke(app, ["done", "1"])
    assert res1.exit_code == 0

    res2 = runner.invoke(app, ["open", "1"])
    assert res2.exit_code == 0

    runner.invoke(app, ["done", "1"])

    # Check JSON to verify state
    res_list = runner.invoke(app, ["list", "--all", "--json"])
    data = json.loads(res_list.stdout)
    assert data[0]["closed_at"] is not None

    # Invalid ID
    res3 = runner.invoke(app, ["done", "999"])
    assert res3.exit_code != 0
    res4 = runner.invoke(app, ["open", "999"])
    assert res4.exit_code != 0


def test_search_command(clean_db):
    runner.invoke(app, ["add", "Alpha bravo"])
    runner.invoke(app, ["add", "Charlie delta"])

    # exact
    res1 = runner.invoke(app, ["search", "Alpha"])
    assert res1.exit_code == 0
    assert "Alpha" in res1.stdout
    assert "Charlie" not in res1.stdout

    # no result
    res2 = runner.invoke(app, ["search", "Zulu"])
    assert res2.exit_code == 0

    # json
    res3 = runner.invoke(app, ["search", "Charlie", "--json"])
    data = json.loads(res3.stdout)
    assert len(data) == 1
    assert data[0]["body"] == "Charlie delta"


def test_remove_and_purge(clean_db):
    runner.invoke(app, ["add", "Note 1"])
    runner.invoke(app, ["add", "Note 2"])

    # Remove existing
    res = runner.invoke(app, ["remove", "1"])
    assert res.exit_code == 0

    # Remove nonexistent
    res = runner.invoke(app, ["remove", "999"])
    assert res.exit_code != 0

    runner.invoke(app, ["done", "2"])

    # Purge
    res = runner.invoke(app, ["purge"])
    assert res.exit_code == 0

    conn = sqlite3.connect(clean_db)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM notes")
    count = cur.fetchone()[0]
    assert count == 0
    conn.close()


def test_show_command(clean_db):
    runner.invoke(app, ["add", "Show me"])

    res1 = runner.invoke(app, ["show", "1"])
    assert res1.exit_code == 0
    assert "Show me" in res1.stdout

    res2 = runner.invoke(app, ["show", "999"])
    assert res2.exit_code != 0

    res3 = runner.invoke(app, ["show", "1", "--json"])
    data = json.loads(res3.stdout)
    assert data[0]["id"] == 1
    assert data[0]["body"] == "Show me"


def test_invalid_ids(clean_db):
    for bad_id in ["0", "-1", "abc", "  "]:
        res = runner.invoke(app, ["show", bad_id])
        assert res.exit_code != 0


def test_version_and_help():
    res = runner.invoke(app, ["--version"])
    assert res.exit_code == 0
    res2 = runner.invoke(app, ["--help"])
    assert res2.exit_code == 0


def test_empty_database_operations(clean_db):
    # Test read operations on completely empty DB
    assert runner.invoke(app, ["list"]).exit_code == 0
    assert runner.invoke(app, ["search", "test"]).exit_code == 0
    assert runner.invoke(app, ["purge"]).exit_code == 0
    assert runner.invoke(app, ["show", "1"]).exit_code != 0
    assert runner.invoke(app, ["remove", "1"]).exit_code != 0
    assert runner.invoke(app, ["edit", "1", "edit"]).exit_code != 0
    assert runner.invoke(app, ["done", "1"]).exit_code != 0
    assert runner.invoke(app, ["open", "1"]).exit_code != 0
