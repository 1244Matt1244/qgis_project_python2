"""Statistical functions for geospatial analysis."""

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from qgis_toolkit.exceptions import ValidationError


@dataclass(frozen=True)
class BoundingBox:
    """Axis-aligned bounding box."""

    min_x: float
    min_y: float
    max_x: float
    max_y: float

    @property
    def width(self) -> float:
        return self.max_x - self.min_x

    @property
    def height(self) -> float:
        return self.max_y - self.min_y

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def center(self) -> tuple[float, float]:
        return ((self.min_x + self.max_x) / 2, (self.min_y + self.max_y) / 2)


@dataclass(frozen=True)
class SummaryStats:
    """Summary statistics for a numeric array."""

    count: int
    min: float
    max: float
    mean: float
    median: float
    std: float
    percentile_25: float
    percentile_75: float


def compute_bounding_box(coords: Sequence[tuple[float, float]]) -> BoundingBox:
    """Compute axis-aligned bounding box from coordinates.

    Args:
        coords: Sequence of (x, y) tuples.

    Returns:
        BoundingBox instance.

    Raises:
        ValidationError: If coords is empty.
    """
    if not coords:
        raise ValidationError("Cannot compute bounding box from empty coordinates")

    arr = np.array(coords, dtype=float)
    if arr.ndim != 2 or arr.shape[1] != 2:
        raise ValidationError(f"Expected Nx2 array, got shape {arr.shape}")

    return BoundingBox(
        min_x=float(arr[:, 0].min()),
        min_y=float(arr[:, 1].min()),
        max_x=float(arr[:, 0].max()),
        max_y=float(arr[:, 1].max()),
    )


def summarize(values: Sequence[float] | np.ndarray) -> SummaryStats:
    """Compute summary statistics for numeric values.

    Args:
        values: Sequence of numeric values.

    Returns:
        SummaryStats instance.

    Raises:
        ValidationError: If values is empty.
    """
    arr = np.asarray(values, dtype=float)
    arr = arr[~np.isnan(arr)]

    if arr.size == 0:
        raise ValidationError("Cannot summarize empty or all-NaN array")

    return SummaryStats(
        count=int(arr.size),
        min=float(arr.min()),
        max=float(arr.max()),
        mean=float(arr.mean()),
        median=float(np.median(arr)),
        std=float(arr.std(ddof=1)) if arr.size > 1 else 0.0,
        percentile_25=float(np.percentile(arr, 25)),
        percentile_75=float(np.percentile(arr, 75)),
    )


def normalize(values: Sequence[float] | np.ndarray) -> np.ndarray:
    """Min-max normalize values to [0, 1].

    Args:
        values: Input array.

    Returns:
        Normalized array.

    Raises:
        ValidationError: If all values are identical.
    """
    arr = np.asarray(values, dtype=float)
    min_v, max_v = float(arr.min()), float(arr.max())

    if max_v - min_v == 0:
        raise ValidationError("Cannot normalize array with constant values")

    return (arr - min_v) / (max_v - min_v)
