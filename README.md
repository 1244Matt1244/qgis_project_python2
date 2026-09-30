# qgis-toolkit

A professional Python toolkit for geospatial analysis — boulder detection, raster sampling, vector statistics, and more. Built as a proper installable package with CLI, tests, and Docker support.

[![CI](https://github.com/1244Matt1244/qgis_project_python2/actions/workflows/ci.yml/badge.svg)](https://github.com/1244Matt1244/qgis_project_python2/actions)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Features

- **Boulder analysis** — dimensions (length, width, height) from polygon + raster, with PCA orientation and Wentworth classification
- **Raster sampling** — mask raster values within polygons, compute statistics (min/max/mean/std/range)
- **Vector metrics** — area, perimeter, centroid, orientation, aspect ratio via PCA
- **Statistical utilities** — bounding box, summary stats, min-max normalization
- **CLI** — built with Typer + Rich for beautiful terminal output
- **Configurable** — Pydantic Settings with `.env` support
- **Structured logging** — JSON or console output via structlog
- **Fully tested** — 30 tests (unit + property-based + CLI integration)

## Installation

### From source (development)

git clone https://github.com/1244Matt1244/qgis_project_python2.git
cd qgis_project_python2
python -m pip install -e ".[dev]"

### With Docker

docker compose up --build

## Quick Start

### CLI

Show available commands:

qgis-toolkit --help

Analyze a boulder from WKT + raster:

qgis-toolkit boulder analyze --polygon "POLYGON ((0 0, 2 0, 2 1, 0 1, 0 0))" --raster bathymetry.tif

Inspect raster metadata:

qgis-toolkit raster info bathymetry.tif

Compute polygon metrics:

qgis-toolkit vector metrics --polygon "POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))"

### Python API

from shapely.geometry import Polygon
from qgis_toolkit import compute_polygon_metrics, analyze_boulder

polygon = Polygon([(0, 0), (2, 0), (2, 1), (0, 1), (0, 0)])
metrics = compute_polygon_metrics(polygon, crs_unit_scale=1.0)
print(f"Area: {metrics.area} m2, Length: {metrics.length} m")

dims = analyze_boulder(
    boulder_id=1,
    polygon=polygon,
    raster_path="bathymetry.tif",
)
print(f"Boulder height: {dims.height_m} m")

## Architecture

src/qgis_toolkit/
    __init__.py          Public API exports
    __version__.py       Version info
    config.py            Pydantic Settings (.env support)
    logging.py           structlog configuration
    exceptions.py        Custom exception hierarchy

    core/                Pure business logic (no QGIS dependency)
        stats.py         Bounding box, summary stats, normalization
        vector.py        Polygon metrics, PCA, validation, simplify
        raster.py        Raster IO, sampling, statistics
        boulder.py       High-level boulder analysis

    cli/                 Command-line interface
        main.py          Typer app entry point
        commands/
            boulder.py   Boulder subcommands
            raster.py    Raster subcommands
            vector.py    Vector subcommands

tests/
    unit/                Fast tests (no QGIS required)
    integration/         CLI integration tests
    data/                Sample GeoJSON/GeoTIFF files

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11+ |
| CLI | Typer + Rich |
| Config | Pydantic Settings v2 |
| Logging | structlog |
| Geometry | Shapely 2.x |
| Raster | rasterio |
| Vector IO | Fiona |
| Numerics | NumPy, scikit-learn |
| Testing | pytest, Hypothesis, typer.testing |
| Linting | Ruff |
| Type checking | mypy (strict mode) |
| Build backend | Hatchling |
| CI | GitHub Actions (Python 3.11 + 3.12) |
| Container | Docker + Docker Compose |

## Development

### Install with dev dependencies

python -m pip install -e ".[dev]"
pre-commit install

### Common commands (via Makefile)

make test              # All tests
make test-unit         # Unit tests only
make test-integration  # Integration tests only
make lint              # Ruff check
make format            # Ruff format + fix
make type-check        # mypy strict
make clean             # Remove build artifacts
make build             # Build wheel + sdist

## Testing

python -m pytest -v
python -m pytest --cov=src/qgis_toolkit --cov-report=term-missing

30 tests total:
- 17 unit tests (validators, metrics, statistics)
- 3 property-based tests (Hypothesis)
- 4 CLI integration tests
- Plus fixtures, parametrization, and edge cases

## Environment Variables

All settings use the QGIS_TOOLKIT_ prefix:

QGIS_TOOLKIT_LOG_LEVEL=INFO
QGIS_TOOLKIT_LOG_FORMAT=json
QGIS_TOOLKIT_MAX_WORKERS=4
QGIS_TOOLKIT_DEFAULT_CRS=EPSG:4326
QGIS_TOOLKIT_BOULDER_MIN_AREA=1.0
QGIS_TOOLKIT_BOULDER_MAX_AREA=10000.0
QGIS_TOOLKIT_BOULDER_HEIGHT_THRESHOLD=0.5

See src/qgis_toolkit/config.py for the full list.

## Project Status

This is version 0.1.0 — early alpha. The core modules are stable and tested, and the CLI is functional. Future plans:
- QGIS plugin wrapper (GUI inside QGIS)
- Cloud-optimized GeoTIFF support
- Batch processing with Dask
- Point cloud (LAS/LAZ) sampling

## License

MIT License — see LICENSE for details.

## Author

Matej Martinović
- GitHub: @1244Matt1244
- Email: matt123.3a@gmail.com
