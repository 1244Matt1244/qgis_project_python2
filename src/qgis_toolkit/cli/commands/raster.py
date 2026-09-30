"""Raster CLI commands."""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from qgis_toolkit.core.raster import read_raster_info
from qgis_toolkit.exceptions import QgisToolkitError

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command("info")
def info(
    raster_path: Annotated[
        Path,
        typer.Argument(
            help="Path to raster file.",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
) -> None:
    """Print raster metadata."""
    try:
        meta = read_raster_info(raster_path)
    except QgisToolkitError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e

    table = Table(title=f"Raster: {raster_path.name}", show_header=False)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Dimensions", f"{meta.width} × {meta.height}")
    table.add_row("Bands", str(meta.count))
    table.add_row("CRS", meta.crs or "N/A")
    table.add_row("Data type", meta.dtype)
    table.add_row("NoData", str(meta.nodata) if meta.nodata is not None else "none")
    table.add_row("Resolution", f"{meta.resolution[0]:.4f}, {meta.resolution[1]:.4f}")
    table.add_row("Bounds", ", ".join(f"{b:.2f}" for b in meta.bounds))

    console.print(table)
