from datetime import UTC, datetime

from jotter.domain.entities.note import Note
from jotter.domain.exceptions import InvalidNoteError
from jotter.domain.repositories import NoteRepository


class NoteService:
    """Application service for coordinating note operations."""

    def __init__(self, repository: NoteRepository):
        self._repo = repository

    def _now(self) -> str:
        return datetime.now(UTC).isoformat()

    def add_note(self, body: str, tag: str = "") -> Note:
        body = body.strip()
        if not body:
            raise InvalidNoteError("Note body cannot be empty.")
        tag = tag.strip()
        return self._repo.add(body, tag, self._now())

    def get_note(self, note_id: int) -> Note:
        return self._repo.get(note_id)

    def list_notes(self, include_closed: bool = False, tag: str = "") -> list[Note]:
        return self._repo.list_notes(include_closed, tag.strip())

    def complete_note(self, note_id: int) -> None:
        self._repo.set_done(note_id, True, self._now())

    def reopen_note(self, note_id: int) -> None:
        self._repo.set_done(note_id, False, None)

    def edit_note(self, note_id: int, body: str, tag: str | None = None) -> None:
        body = body.strip()
        if not body:
            raise InvalidNoteError("Note body cannot be empty.")
        if tag is not None:
            tag = tag.strip()
        self._repo.edit(note_id, body, tag)

    def remove_note(self, note_id: int) -> None:
        self._repo.remove(note_id)

    def purge_closed_notes(self) -> int:
        return self._repo.purge()

    def search_notes(self, query: str, include_closed: bool = False) -> list[Note]:
        if not query:
            return []
        return self._repo.search(query, include_closed)
