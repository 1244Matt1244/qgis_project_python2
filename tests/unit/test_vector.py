"""Unit tests for qgis_toolkit.core.vector."""

import math

import pytest
from shapely.geometry import MultiPolygon, Point, Polygon

from qgis_toolkit.core.vector import (
    compute_polygon_metrics,
    ensure_polygon,
    polygon_bbox_center,
    polygon_bounds,
    simplify_polygon,
    validate_geometry,
)
from qgis_toolkit.exceptions import GeometryError

pytestmark = pytest.mark.unit


class TestValidateGeometry:
    def test_none_raises(self) -> None:
        with pytest.raises(GeometryError, match="None"):
            validate_geometry(None)  # type: ignore[arg-type]

    def test_empty_raises(self) -> None:
        with pytest.raises(GeometryError, match="empty"):
            validate_geometry(Polygon())

    def test_valid_geometry(self, square_polygon: Polygon) -> None:
        assert validate_geometry(square_polygon) is square_polygon


class TestEnsurePolygon:
    def test_returns_polygon(self, square_polygon: Polygon) -> None:
        assert ensure_polygon(square_polygon) == square_polygon

    def test_multipolygon_with_one(self, square_polygon: Polygon) -> None:
        mp = MultiPolygon([square_polygon])
        result = ensure_polygon(mp)
        assert result == square_polygon

    def test_point_raises(self) -> None:
        with pytest.raises(GeometryError, match="Polygon"):
            ensure_polygon(Point(0, 0))


class TestComputePolygonMetrics:
    def test_square(self, square_polygon: Polygon) -> None:
        m = compute_polygon_metrics(square_polygon)
        assert m.area == 1.0
        assert m.perimeter == 4.0
        assert m.centroid_x == pytest.approx(0.5)
        assert m.centroid_y == pytest.approx(0.5)

    def test_rectangle_aspect_ratio(self, rectangle_polygon: Polygon) -> None:
        m = compute_polygon_metrics(rectangle_polygon)
        assert m.area == 2.0
        assert m.length == pytest.approx(2.0, rel=0.01)
        assert m.width == pytest.approx(1.0, rel=0.01)
        assert m.aspect_ratio == pytest.approx(2.0, rel=0.01)

    def test_unit_scale(self, square_polygon: Polygon) -> None:
        m = compute_polygon_metrics(square_polygon, crs_unit_scale=1000.0)
        assert m.area == 1_000_000.0
        assert m.perimeter == 4000.0


class TestBounds:
    def test_polygon_bounds(self, square_polygon: Polygon) -> None:
        bounds = polygon_bounds(square_polygon)
        assert bounds == (0.0, 0.0, 1.0, 1.0)

    def test_bbox_center(self, square_polygon: Polygon) -> None:
        cx, cy = polygon_bbox_center(square_polygon)
        assert cx == 0.5
        assert cy == 0.5


class TestSimplify:
    def test_simplify_reduces_vertices(self) -> None:
        dense = Polygon([(i * 0.01, 0) for i in range(100)] + [(1, 1), (0, 1), (0, 0)])
        simplified = simplify_polygon(dense, tolerance=0.05)
        assert len(simplified.exterior.coords) < len(dense.exterior.coords)

    def test_negative_tolerance_raises(self, square_polygon: Polygon) -> None:
        with pytest.raises(GeometryError, match="Tolerance"):
            simplify_polygon(square_polygon, tolerance=-1.0)
