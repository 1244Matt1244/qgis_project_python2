"""Boulder analysis CLI commands."""

import json
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from qgis_toolkit.core.boulder import analyze_boulder, classify_boulder
from qgis_toolkit.exceptions import QgisToolkitError

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.command("analyze")
def analyze(
    polygon_wkt: Annotated[
        str,
        typer.Option("--polygon", "-p", help="Polygon in WKT format."),
    ],
    raster_path: Annotated[
        Path,
        typer.Option(
            "--raster",
            "-r",
            help="Path to raster (GeoTIFF).",
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    boulder_id: Annotated[int, typer.Option("--id", help="Boulder ID.")] = 1,
    band: Annotated[int, typer.Option("--band", "-b", help="Raster band (1-based).")] = 1,
    unit_scale: Annotated[
        float,
        typer.Option("--unit-scale", help="Scale factor to meters (e.g., 0.001 for mm)."),
    ] = 1.0,
    output_json: Annotated[
        bool,
        typer.Option("--json", help="Output as JSON instead of table."),
    ] = False,
) -> None:
    """Analyze a single boulder from WKT polygon and raster."""
    from shapely import wkt as shapely_wkt

    try:
        polygon = shapely_wkt.loads(polygon_wkt)
    except Exception as e:
        console.print(f"[red]Invalid WKT:[/red] {e}")
        raise typer.Exit(1) from e

    try:
        dims = analyze_boulder(
            boulder_id=boulder_id,
            polygon=polygon,
            raster_path=raster_path,
            band=band,
            crs_unit_scale=unit_scale,
        )
    except QgisToolkitError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e

    classification = classify_boulder(dims)

    if output_json:
        console.print_json(
            json.dumps(
                {
                    "id": dims.id,
                    "area_m2": dims.area_m2,
                    "length_m": dims.length_m,
                    "width_m": dims.width_m,
                    "height_m": dims.height_m,
                    "orientation_deg": dims.orientation_deg,
                    "aspect_ratio": dims.aspect_ratio,
                    "classification": classification,
                },
                indent=2,
            )
        )
        return

    table = Table(title=f"Boulder #{dims.id}", show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Area", f"{dims.area_m2:.2f} m²")
    table.add_row("Length", f"{dims.length_m:.2f} m")
    table.add_row("Width", f"{dims.width_m:.2f} m")
    table.add_row("Height", f"{dims.height_m:.2f} m")
    table.add_row("Orientation", f"{dims.orientation_deg:.1f}°")
    table.add_row("Aspect ratio", f"{dims.aspect_ratio:.2f}")
    table.add_row("Pixels", str(dims.pixel_count))
    table.add_row("Classification", f"[bold]{classification}[/bold]")

    console.print(table)
