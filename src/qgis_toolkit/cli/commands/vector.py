"""Vector CLI commands."""

from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from qgis_toolkit.core.vector import compute_polygon_metrics
from qgis_toolkit.exceptions import QgisToolkitError

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command("metrics")
def metrics(
    polygon_wkt: Annotated[
        str,
        typer.Option("--polygon", "-p", help="Polygon in WKT format."),
    ],
    unit_scale: Annotated[
        float,
        typer.Option("--unit-scale", help="Scale factor to meters."),
    ] = 1.0,
) -> None:
    """Compute polygon metrics from WKT."""
    from shapely import wkt as shapely_wkt

    try:
        polygon = shapely_wkt.loads(polygon_wkt)
    except Exception as e:
        console.print(f"[red]Invalid WKT:[/red] {e}")
        raise typer.Exit(1) from e

    try:
        m = compute_polygon_metrics(polygon, unit_scale)
    except QgisToolkitError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e

    table = Table(title="Polygon Metrics", show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Area", f"{m.area:.4f}")
    table.add_row("Perimeter", f"{m.perimeter:.4f}")
    table.add_row("Centroid", f"({m.centroid_x:.4f}, {m.centroid_y:.4f})")
    table.add_row("Length", f"{m.length:.4f}")
    table.add_row("Width", f"{m.width:.4f}")
    table.add_row("Orientation", f"{m.orientation_deg:.2f}°")
    table.add_row("Aspect ratio", f"{m.aspect_ratio:.3f}")

    console.print(table)
