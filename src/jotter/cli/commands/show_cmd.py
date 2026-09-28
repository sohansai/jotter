import sys

import typer

from jotter.domain.exceptions import JotterError
from jotter.presentation.console import console, print_error
from jotter.presentation.formatters.json import format_note_json
from jotter.presentation.formatters.table import build_notes_table


def execute(
    ctx: typer.Context,
    note_id: int = typer.Argument(..., help="ID of the note to view"),
    as_json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """View details of a specific note."""
    service = ctx.obj.note_service

    try:
        note = service.get_note(note_id)
        if as_json:
            print(format_note_json(note))
        else:
            console.print(build_notes_table([note]))
    except JotterError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Failed to get note: {e}")
        sys.exit(1)
