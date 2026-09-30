"""Pytest fixtures shared across test suites."""

import numpy as np
import pytest
from shapely.geometry import Polygon


@pytest.fixture
def square_polygon() -> Polygon:
    """Unit square polygon."""
    return Polygon([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)])


@pytest.fixture
def rectangle_polygon() -> Polygon:
    """2x1 rectangle."""
    return Polygon([(0, 0), (2, 0), (2, 1), (0, 1), (0, 0)])


@pytest.fixture
def sample_coords() -> list[tuple[float, float]]:
    return [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]


@pytest.fixture
def sample_values() -> list[float]:
    return [1.0, 2.0, 3.0, 4.0, 5.0]


@pytest.fixture
def sample_array() -> np.ndarray:
    return np.array([[0.0, 1.0], [2.0, 3.0], [4.0, 5.0]])
