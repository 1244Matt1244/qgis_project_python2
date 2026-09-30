"""qgis-toolkit: Professional QGIS Python toolkit for geospatial analysis."""

from qgis_toolkit.__version__ import __version__
from qgis_toolkit.config import Settings, get_settings
from qgis_toolkit.core import (
    BoulderDimensions,
    RasterInfo,
    RasterStats,
    SummaryStats,
    analyze_boulder,
    classify_boulder,
    compute_bounding_box,
    compute_polygon_metrics,
    compute_raster_stats,
    ensure_polygon,
    read_raster_info,
    sample_raster_in_polygon,
    summarize,
)
from qgis_toolkit.exceptions import (
    GeometryError,
    ProcessingError,
    QgisToolkitError,
    RasterError,
    ValidationError,
)
from qgis_toolkit.logging import configure_logging, get_logger

__all__ = [
    "__version__",
    # config
    "Settings",
    "get_settings",
    # logging
    "configure_logging",
    "get_logger",
    # exceptions
    "QgisToolkitError",
    "GeometryError",
    "RasterError",
    "ValidationError",
    "ProcessingError",
    # core - boulder
    "BoulderDimensions",
    "analyze_boulder",
    "classify_boulder",
    # core - raster
    "RasterInfo",
    "RasterStats",
    "compute_raster_stats",
    "read_raster_info",
    "sample_raster_in_polygon",
    # core - stats
    "SummaryStats",
    "compute_bounding_box",
    "summarize",
    # core - vector
    "compute_polygon_metrics",
    "ensure_polygon",
]
