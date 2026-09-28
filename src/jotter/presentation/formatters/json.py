import json

from jotter.domain.entities.note import Note


def format_notes_json(notes: list[Note]) -> str:
    """Format notes as JSON string."""
    data = []
    for note in notes:
        data.append(
            {
                "id": note.id,
                "body": note.body,
                "tag": note.tag,
                "done": note.done,
                "added_at": note.added_at.isoformat(),
                "closed_at": note.closed_at.isoformat() if note.closed_at else None,
            }
        )
    return json.dumps(data, indent=2)


def format_note_json(note: Note) -> str:
    """Format single note as JSON string."""
    return format_notes_json([note])
