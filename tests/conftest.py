import os
from pathlib import Path

import pytest

from jotter.application.services.note_service import NoteService
from jotter.infrastructure.database.connection import get_connection
from jotter.infrastructure.database.migrations import run_migrations
from jotter.infrastructure.repositories.sqlite_note_repository import SQLiteNoteRepository


@pytest.fixture
def temp_db_path(tmp_path: Path):
    db_file = tmp_path / "jotter.db"
    os.environ["JOTTER_DB"] = str(db_file)
    yield db_file
    if "JOTTER_DB" in os.environ:
        del os.environ["JOTTER_DB"]


@pytest.fixture
def db_connection(temp_db_path: Path):
    conn = get_connection(temp_db_path)
    run_migrations(conn)
    yield conn
    conn.close()


@pytest.fixture
def repository(db_connection):
    return SQLiteNoteRepository(db_connection)


@pytest.fixture
def note_service(repository):
    return NoteService(repository)
