from datetime import UTC, datetime

from rich.table import Table

from jotter.domain.entities.note import Note


def _format_age(dt: datetime) -> str:
    now = datetime.now(UTC)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)

    diff = now - dt
    total_seconds = int(diff.total_seconds())

    if total_seconds < 60:
        return "just now"
    elif total_seconds < 3600:
        return f"{total_seconds // 60}m"
    elif total_seconds < 86400:
        return f"{total_seconds // 3600}h"
    else:
        return f"{total_seconds // 86400}d"


def build_notes_table(notes: list[Note]) -> Table:
    table = Table(box=None, show_header=True, header_style="bold")
    table.add_column("ID", style="cyan")
    table.add_column("AGE", style="blue")
    table.add_column("TAG", style="magenta")
    table.add_column("NOTE")

    for note in notes:
        mark = "[dim]~[/dim] " if note.done else ""
        tag_col = note.tag if note.tag else "-"
        row_style = "dim" if note.done else ""

        table.add_row(
            str(note.id), _format_age(note.added_at), tag_col, f"{mark}{note.body}", style=row_style
        )
    return table
