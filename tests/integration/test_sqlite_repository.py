from datetime import UTC, datetime

import pytest

from jotter.domain.exceptions import NoteNotFoundError
from jotter.infrastructure.repositories.sqlite_note_repository import SQLiteNoteRepository


def test_repository_crud(repository: SQLiteNoteRepository):
    # Add
    now = datetime.now(UTC).isoformat()
    note = repository.add("test note", "tag1", now)
    assert note.id == 1
    assert note.body == "test note"

    # Get
    fetched = repository.get(1)
    assert fetched.body == "test note"

    # List
    notes = repository.list_notes()
    assert len(notes) == 1

    # Update
    repository.set_done(1, True, now)
    assert repository.get(1).done is True

    # Edit
    repository.edit(1, "updated", "tag2")
    assert repository.get(1).body == "updated"
    assert repository.get(1).tag == "tag2"

    # Search
    results = repository.search("update", include_closed=True)
    assert len(results) == 1

    # Remove
    repository.remove(1)
    with pytest.raises(NoteNotFoundError):
        repository.get(1)
