import sys

import typer

from jotter.presentation.console import console, print_empty_state, print_error
from jotter.presentation.formatters.json import format_notes_json
from jotter.presentation.formatters.table import build_notes_table


def execute(
    ctx: typer.Context,
    query: str = typer.Argument(..., help="Text to search for in notes"),
    all_notes: bool = typer.Option(False, "--all", "-a", help="Include closed notes in search"),
    as_json: bool = typer.Option(False, "--json", help="Output as JSON"),
):
    """Search notes by content."""
    service = ctx.obj.note_service

    try:
        notes = service.search_notes(query, all_notes)
        if as_json:
            print(format_notes_json(notes))
        else:
            if not notes:
                print_empty_state("No matching notes found.")
            else:
                console.print(build_notes_table(notes))
    except Exception as e:
        print_error(f"Search failed: {e}")
        sys.exit(1)
