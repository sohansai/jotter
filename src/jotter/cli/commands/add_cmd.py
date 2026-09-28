import sys

import typer

from jotter.domain.exceptions import JotterError
from jotter.presentation.console import print_error, print_success


def execute(
    ctx: typer.Context,
    text: list[str] = typer.Argument(..., help="The body of the note"),
    tag: str = typer.Option("", "--tag", "-t", help="Tag to organize notes"),
):
    """Add a new note."""
    service = ctx.obj.note_service
    body = " ".join(text).strip()

    try:
        note = service.add_note(body, tag)
        print_success(f"Added #{note.id}")
    except JotterError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Failed to add note: {e}")
        sys.exit(1)
