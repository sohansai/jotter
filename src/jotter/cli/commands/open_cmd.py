import sys

import typer

from jotter.domain.exceptions import JotterError
from jotter.presentation.console import print_error, print_success


def execute(
    ctx: typer.Context,
    note_id: int = typer.Argument(..., help="ID of the note to reopen"),
):
    """Reopen a closed note (alias: undone)."""
    service = ctx.obj.note_service

    try:
        service.reopen_note(note_id)
        print_success(f"Reopened #{note_id}")
    except JotterError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Failed to open note: {e}")
        sys.exit(1)
