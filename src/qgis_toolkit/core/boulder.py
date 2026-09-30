"""Boulder dimension analysis combining vector and raster data."""

from dataclasses import dataclass
from pathlib import Path

from shapely.geometry import Polygon

from qgis_toolkit.config import get_settings
from qgis_toolkit.core.raster import compute_raster_stats
from qgis_toolkit.core.vector import (
    compute_polygon_metrics,
    ensure_polygon,
)
from qgis_toolkit.exceptions import ProcessingError
from qgis_toolkit.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class BoulderDimensions:
    """Full dimensions of a boulder."""

    id: int
    area_m2: float
    length_m: float
    width_m: float
    height_m: float
    centroid_x: float
    centroid_y: float
    orientation_deg: float
    aspect_ratio: float
    pixel_count: int


def analyze_boulder(
    boulder_id: int,
    polygon: Polygon,
    raster_path: str | Path,
    band: int = 1,
    crs_unit_scale: float = 1.0,
) -> BoulderDimensions:
    """Analyze a single boulder: dimensions from vector + height from raster.

    Args:
        boulder_id: Unique identifier.
        polygon: Boulder footprint polygon.
        raster_path: Path to bathymetric raster.
        band: Raster band (1-based).
        crs_unit_scale: Factor to convert to meters (e.g., 0.001 for mm).

    Returns:
        BoulderDimensions.

    Raises:
        ProcessingError: If analysis fails.
    """
    settings = get_settings()

    try:
        polygon = ensure_polygon(polygon)
    except Exception as e:
        raise ProcessingError(f"Invalid boulder geometry {boulder_id}: {e}") from e

    metrics = compute_polygon_metrics(polygon, crs_unit_scale)

    if metrics.area < settings.boulder_min_area:
        raise ProcessingError(
            f"Boulder {boulder_id} area {metrics.area:.2f} m² < min {settings.boulder_min_area}"
        )

    if metrics.area > settings.boulder_max_area:
        raise ProcessingError(
            f"Boulder {boulder_id} area {metrics.area:.2f} m² > max {settings.boulder_max_area}"
        )

    try:
        raster_stats = compute_raster_stats(raster_path, polygon, band)
    except Exception as e:
        raise ProcessingError(f"Raster sampling failed for boulder {boulder_id}: {e}") from e

    if raster_stats.height_range < settings.boulder_height_threshold:
        logger.warning(
            "boulder_below_height_threshold",
            boulder_id=boulder_id,
            height=raster_stats.height_range,
            threshold=settings.boulder_height_threshold,
        )

    return BoulderDimensions(
        id=boulder_id,
        area_m2=metrics.area,
        length_m=metrics.length,
        width_m=metrics.width,
        height_m=raster_stats.height_range,
        centroid_x=metrics.centroid_x,
        centroid_y=metrics.centroid_y,
        orientation_deg=metrics.orientation_deg,
        aspect_ratio=metrics.aspect_ratio,
        pixel_count=raster_stats.count,
    )


def classify_boulder(dimensions: BoulderDimensions) -> str:
    """Classify boulder based on size (Wentworth-style).

    Args:
        dimensions: BoulderDimensions.

    Returns:
        Classification string.
    """
    d = dimensions.length_m
    if d < 0.256:
        return "pebble"
    if d < 0.5:
        return "cobble"
    if d < 1.0:
        return "small_boulder"
    if d < 2.0:
        return "medium_boulder"
    if d < 4.0:
        return "large_boulder"
    return "very_large_boulder"
