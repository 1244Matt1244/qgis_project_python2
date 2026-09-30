"""Core processing modules."""

from qgis_toolkit.core.boulder import (
    BoulderDimensions,
    analyze_boulder,
    classify_boulder,
)
from qgis_toolkit.core.raster import (
    RasterInfo,
    RasterStats,
    compute_raster_stats,
    read_raster_info,
    sample_raster_in_polygon,
)
from qgis_toolkit.core.stats import (
    BoundingBox,
    SummaryStats,
    compute_bounding_box,
    normalize,
    summarize,
)
from qgis_toolkit.core.vector import (
    PolygonMetrics,
    compute_polygon_metrics,
    ensure_polygon,
    polygon_bbox_center,
    polygon_bounds,
    simplify_polygon,
    validate_geometry,
)

__all__ = [
    # boulder
    "BoulderDimensions",
    "analyze_boulder",
    "classify_boulder",
    # raster
    "RasterInfo",
    "RasterStats",
    "compute_raster_stats",
    "read_raster_info",
    "sample_raster_in_polygon",
    # stats
    "BoundingBox",
    "SummaryStats",
    "compute_bounding_box",
    "normalize",
    "summarize",
    # vector
    "PolygonMetrics",
    "compute_polygon_metrics",
    "ensure_polygon",
    "polygon_bbox_center",
    "polygon_bounds",
    "simplify_polygon",
    "validate_geometry",
]
