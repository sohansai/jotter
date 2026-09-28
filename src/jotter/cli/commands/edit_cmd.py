import sys

import typer

from jotter.domain.exceptions import JotterError
from jotter.presentation.console import print_error, print_success


def execute(
    ctx: typer.Context,
    note_id: int = typer.Argument(..., help="ID of the note to edit"),
    body: str = typer.Option(..., "--body", "-b", help="New body text for the note"),
    tag: str | None = typer.Option(None, "--tag", "-t", help="New tag for the note"),
):
    """Edit an existing note."""
    service = ctx.obj.note_service

    try:
        service.edit_note(note_id, body, tag)
        print_success(f"Edited #{note_id}")
    except JotterError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Failed to edit note: {e}")
        sys.exit(1)
