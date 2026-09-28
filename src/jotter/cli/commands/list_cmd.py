import sys

import typer

from jotter.presentation.console import console, print_empty_state, print_error
from jotter.presentation.formatters.json import format_notes_json
from jotter.presentation.formatters.table import build_notes_table


def execute(
    ctx: typer.Context,
    all_notes: bool = typer.Option(False, "--all", "-a", help="Include closed notes"),
    tag: str = typer.Option("", "--tag", "-t", help="Only show notes with this tag"),
    as_json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """List open notes (alias: ls)."""
    service = ctx.obj.note_service

    try:
        notes = service.list_notes(all_notes, tag)
        if as_json:
            print(format_notes_json(notes))
        else:
            if not notes:
                print_empty_state()
            else:
                console.print(build_notes_table(notes))
    except Exception as e:
        print_error(f"Failed to list notes: {e}")
        sys.exit(1)
