"""Unit tests for qgis_toolkit.core.stats."""

import numpy as np
import pytest

from qgis_toolkit.core.stats import (
    BoundingBox,
    compute_bounding_box,
    normalize,
    summarize,
)
from qgis_toolkit.exceptions import ValidationError

pytestmark = pytest.mark.unit


class TestBoundingBox:
    def test_properties(self) -> None:
        bbox = BoundingBox(min_x=0, min_y=0, max_x=4, max_y=2)
        assert bbox.width == 4
        assert bbox.height == 2
        assert bbox.area == 8
        assert bbox.center == (2.0, 1.0)


class TestComputeBoundingBox:
    def test_from_coords(self, sample_coords: list[tuple[float, float]]) -> None:
        bbox = compute_bounding_box(sample_coords)
        assert bbox.min_x == 0.0
        assert bbox.min_y == 0.0
        assert bbox.max_x == 1.0
        assert bbox.max_y == 1.0

    def test_empty_coords_raises(self) -> None:
        with pytest.raises(ValidationError, match="empty"):
            compute_bounding_box([])

    def test_invalid_shape_raises(self) -> None:
        with pytest.raises(ValidationError, match="Nx2"):
            compute_bounding_box([(0.0,), (1.0,)])


class TestSummarize:
    def test_basic_stats(self, sample_values: list[float]) -> None:
        stats = summarize(sample_values)
        assert stats.count == 5
        assert stats.min == 1.0
        assert stats.max == 5.0
        assert stats.mean == 3.0
        assert stats.median == 3.0

    def test_ignores_nan(self) -> None:
        values = [1.0, 2.0, np.nan, 4.0]
        stats = summarize(values)
        assert stats.count == 3

    def test_empty_raises(self) -> None:
        with pytest.raises(ValidationError):
            summarize([])

    def test_all_nan_raises(self) -> None:
        with pytest.raises(ValidationError):
            summarize([np.nan, np.nan])


class TestNormalize:
    def test_normalizes_to_0_1(self) -> None:
        result = normalize([0.0, 5.0, 10.0])
        assert result[0] == 0.0
        assert result[1] == 0.5
        assert result[2] == 1.0

    def test_constant_raises(self) -> None:
        with pytest.raises(ValidationError):
            normalize([5.0, 5.0, 5.0])
