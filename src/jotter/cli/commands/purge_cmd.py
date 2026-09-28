import sys

import typer

from jotter.presentation.console import print_error, print_success


def execute(
    ctx: typer.Context,
):
    """Delete every closed note."""
    service = ctx.obj.note_service

    try:
        count = service.purge_closed_notes()
        print_success(f"Removed {count} closed note(s)")
    except Exception as e:
        print_error(f"Failed to purge notes: {e}")
        sys.exit(1)
