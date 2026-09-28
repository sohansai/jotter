import sys

# Force UTF-8 encoding on Windows to prevent charmap crashes for all entrypoints,
# including the installed console-script entrypoint rather than only `python -m jotter`.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import typer

from jotter import __version__
from jotter.application.services.note_service import NoteService

# Import commands to register them
from jotter.cli.commands import (
    add_cmd,
    done_cmd,
    edit_cmd,
    list_cmd,
    open_cmd,
    purge_cmd,
    remove_cmd,
    search_cmd,
    show_cmd,
)
from jotter.cli.context import AppContext
from jotter.configuration.settings import get_db_path
from jotter.infrastructure.database.connection import get_connection
from jotter.infrastructure.database.migrations import run_migrations
from jotter.infrastructure.repositories.sqlite_note_repository import SQLiteNoteRepository
from jotter.presentation.console import print_error

app = typer.Typer(
    help="jotter - sticky notes that stay in your terminal",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
)


def _setup_context(ctx: typer.Context):
    """Initialize dependencies and inject into Typer context."""
    if ctx.obj is None:
        ctx.obj = AppContext()

    try:
        db_path = get_db_path()
        conn = get_connection(db_path)
        run_migrations(conn)
        repo = SQLiteNoteRepository(conn)
        ctx.obj.note_service = NoteService(repo)
    except Exception as e:
        print_error(f"Failed to initialize database: {e}")
        sys.exit(1)


def version_callback(value: bool):
    if value:
        typer.echo(f"jotter {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    version: bool | None = typer.Option(
        None,
        "--version",
        help="Print the version and exit",
        callback=version_callback,
        is_eager=True,
    ),
):
    """jotter - sticky notes that stay in your terminal"""
    _setup_context(ctx)


# Register Commands
app.command(name="add")(add_cmd.execute)
app.command(name="list")(list_cmd.execute)
app.command(name="ls", hidden=True)(list_cmd.execute)
app.command(name="done")(done_cmd.execute)
app.command(name="open")(open_cmd.execute)
app.command(name="undone", hidden=True)(open_cmd.execute)
app.command(name="remove")(remove_cmd.execute)
app.command(name="rm", hidden=True)(remove_cmd.execute)
app.command(name="purge")(purge_cmd.execute)
app.command(name="show")(show_cmd.execute)
app.command(name="edit")(edit_cmd.execute)
app.command(name="search")(search_cmd.execute)
