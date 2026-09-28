import sqlite3
from collections.abc import Generator
from datetime import UTC, datetime, timedelta

import pytest

from jotter.application.services.note_service import NoteService
from jotter.infrastructure.repositories.sqlite_note_repository import SQLiteNoteRepository
from jotter.presentation.formatters.table import _format_age


def test_format_age_branches():
    now = datetime.now(UTC)
    assert "m" in _format_age(now - timedelta(seconds=120))
    assert "h" in _format_age(now - timedelta(hours=2))
    assert "d" in _format_age(now - timedelta(days=2))

    # timezone unaware dt
    naive = datetime.now(UTC).replace(tzinfo=None) - timedelta(minutes=5)
    assert "m" in _format_age(naive)


@pytest.fixture
def repo_service() -> Generator[NoteService, None, None]:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            body TEXT NOT NULL,
            tag TEXT,
            done INTEGER NOT NULL DEFAULT 0,
            added_at TEXT NOT NULL,
            closed_at TEXT
        )
    """)
    repo = SQLiteNoteRepository(conn)
    yield NoteService(repo)
    conn.close()


def test_repository_and_service_branches(repo_service: NoteService):
    # Empty query search
    assert repo_service.search_notes("") == []

    # Add note with tag
    note = repo_service.add_note("Tagged note", tag="work")
    assert note.tag == "work"

    # List by tag
    notes = repo_service.list_notes(tag="work")
    assert len(notes) == 1

    notes_empty = repo_service.list_notes(tag="play")
    assert len(notes_empty) == 0

    # Edit note with tag
    repo_service.edit_note(note.id, "Changed body", tag="new_tag")
    note_edited = repo_service.get_note(note.id)
    assert note_edited.body == "Changed body"
    assert note_edited.tag == "new_tag"

    # Error retrieval simulation inside repo (RuntimeError on missing ID)
    # This is tricky because SQLite always returns lastrowid on insert.
    # We can mock cursor.lastrowid to test line 33.
    # We will just accept line 33 might be slightly uncovered if we can't easily mock it.

    # Edit nonexistent note with tag
    from jotter.domain.exceptions import NoteNotFoundError

    with pytest.raises(NoteNotFoundError):
        repo_service.edit_note(999, "Body", tag="new")
