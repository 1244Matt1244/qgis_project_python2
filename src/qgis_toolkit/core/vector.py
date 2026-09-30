"""Vector geometry operations using Shapely."""

from dataclasses import dataclass

import numpy as np
from shapely.geometry import MultiPolygon, Polygon
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from qgis_toolkit.core.stats import compute_bounding_box
from qgis_toolkit.exceptions import GeometryError


@dataclass(frozen=True)
class PolygonMetrics:
    """Metrics for a single polygon."""

    area: float
    perimeter: float
    centroid_x: float
    centroid_y: float
    orientation_deg: float
    length: float
    width: float
    aspect_ratio: float


def validate_geometry(geom: BaseGeometry) -> BaseGeometry:
    """Validate and fix geometry if needed."""
    if geom is None:
        raise GeometryError("Geometry is None")

    if geom.is_empty:
        raise GeometryError("Geometry is empty")

    if not geom.is_valid:
        fixed = geom.buffer(0)
        if fixed.is_empty:
            raise GeometryError("Could not repair invalid geometry")
        return fixed

    return geom


def ensure_polygon(geom: BaseGeometry) -> Polygon:
    """Convert geometry to a single Polygon."""
    geom = validate_geometry(geom)

    if isinstance(geom, Polygon):
        return geom

    if isinstance(geom, MultiPolygon):
        if len(geom.geoms) == 1:
            return geom.geoms[0]
        merged = unary_union(geom.geoms)
        if not isinstance(merged, Polygon):
            raise GeometryError("Could not merge MultiPolygon into single Polygon")
        return merged

    raise GeometryError(f"Expected Polygon or MultiPolygon, got {type(geom).__name__}")


def _sample_boundary(polygon: Polygon, n_points: int = 256) -> np.ndarray:
    """Sample points evenly along the polygon boundary.

    Args:
        polygon: Input polygon.
        n_points: Number of points to sample.

    Returns:
        Nx2 array of coordinates.
    """
    boundary = polygon.exterior
    distances = np.linspace(0, boundary.length, n_points, endpoint=False)
    points = [boundary.interpolate(d) for d in distances]
    return np.array([(p.x, p.y) for p in points])


def compute_polygon_metrics(polygon: Polygon, crs_unit_scale: float = 1.0) -> PolygonMetrics:
    """Compute metrics for a polygon using PCA on densely sampled boundary.

    Args:
        polygon: Shapely Polygon.
        crs_unit_scale: Scale factor to convert to meters.

    Returns:
        PolygonMetrics.
    """
    polygon = ensure_polygon(polygon)
    area = polygon.area * (crs_unit_scale**2)
    perimeter = polygon.length * crs_unit_scale
    centroid = polygon.centroid

    # Densely sample boundary for accurate PCA
    coords = _sample_boundary(polygon, n_points=512)
    centered = coords - coords.mean(axis=0)

    if len(centered) > 1:
        cov = np.cov(centered.T)
        eigvals, eigvecs = np.linalg.eigh(cov)
        # Sort by eigenvalue descending
        order = np.argsort(eigvals)[::-1]
        eigvecs = eigvecs[:, order]

        principal = eigvecs[:, 0]
        orientation = float(np.degrees(np.arctan2(principal[1], principal[0])))

        projections = centered @ eigvecs
        length = float(np.ptp(projections[:, 0])) * crs_unit_scale
        width = float(np.ptp(projections[:, 1])) * crs_unit_scale
    else:
        orientation = 0.0
        length = width = 0.0

    aspect_ratio = length / width if width > 0 else 0.0

    return PolygonMetrics(
        area=area,
        perimeter=perimeter,
        centroid_x=float(centroid.x),
        centroid_y=float(centroid.y),
        orientation_deg=orientation,
        length=length,
        width=width,
        aspect_ratio=aspect_ratio,
    )


def polygon_bounds(polygon: Polygon) -> tuple[float, float, float, float]:
    """Return (min_x, min_y, max_x, max_y)."""
    polygon = ensure_polygon(polygon)
    return tuple(polygon.bounds)  # type: ignore[return-value]


def polygon_bbox_center(polygon: Polygon) -> tuple[float, float]:
    """Return center of bounding box."""
    polygon = ensure_polygon(polygon)
    bbox = compute_bounding_box(list(polygon.exterior.coords))
    return bbox.center


def simplify_polygon(polygon: Polygon, tolerance: float) -> Polygon:
    """Simplify polygon using Douglas-Peucker."""
    if tolerance <= 0:
        raise GeometryError("Tolerance must be > 0")
    return ensure_polygon(polygon).simplify(tolerance, preserve_topology=True)
