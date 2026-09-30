"""Main CLI entry point using Typer."""

import sys
from typing import Annotated

import typer
from rich.console import Console

from qgis_toolkit.__version__ import __version__
from qgis_toolkit.cli.commands import boulder, raster, vector
from qgis_toolkit.logging import configure_logging

app = typer.Typer(
    name="qgis-toolkit",
    help="Professional QGIS Python toolkit for geospatial analysis.",
    add_completion=True,
    no_args_is_help=True,
    rich_markup_mode="rich",
)

console = Console()


def version_callback(value: bool) -> None:
    if value:
        console.print(f"[bold cyan]qgis-toolkit[/bold cyan] version [green]{__version__}[/green]")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-V",
            help="Show version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose (DEBUG) logging."),
    ] = False,
    log_format: Annotated[
        str,
        typer.Option(
            "--log-format",
            help="Log format: console or json.",
            case_sensitive=False,
        ),
    ] = "console",
) -> None:
    """qgis-toolkit: geospatial analysis from the command line."""
    level = "DEBUG" if verbose else "INFO"
    configure_logging(level=level, log_format=log_format)


app.add_typer(boulder.app, name="boulder", help="Boulder dimension analysis.")
app.add_typer(raster.app, name="raster", help="Raster sampling and statistics.")
app.add_typer(vector.app, name="vector", help="Vector geometry operations.")


if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")
        sys.exit(130)
