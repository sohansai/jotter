class JotterError(Exception):
    """Base exception for all Jotter errors."""


class NoteNotFoundError(JotterError):
    """Raised when a note ID does not exist."""

    def __init__(self, note_id: int):
        self.note_id = note_id
        super().__init__(f"Note {note_id} not found.")


class InvalidNoteError(JotterError):
    """Raised when note data is invalid."""
