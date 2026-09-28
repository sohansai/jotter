from rich.console import Console

console = Console()
err_console = Console(stderr=True)


def print_success(message: str) -> None:
    console.print(f"[green]✓[/green] {message}")


def print_error(message: str) -> None:
    err_console.print(f"jotter: [red]error:[/red] {message}")


def print_empty_state(message: str = "Nothing open. Enjoy it while it lasts.") -> None:
    console.print(message, style="italic green")
