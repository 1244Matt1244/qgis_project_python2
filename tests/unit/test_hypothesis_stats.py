"""Property-based tests using Hypothesis."""

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from qgis_toolkit.core.stats import summarize
from qgis_toolkit.exceptions import ValidationError

pytestmark = pytest.mark.unit


@given(values=st.lists(st.floats(min_value=-1e6, max_value=1e6, allow_nan=False), min_size=1, max_size=100))
@settings(max_examples=50)
def test_summarize_min_max_invariant(values: list[float]) -> None:
    stats = summarize(values)
    assert stats.min <= stats.mean <= stats.max
    assert stats.min <= stats.median <= stats.max
    assert stats.count == len(values)


@given(values=st.lists(st.floats(min_value=-100, max_value=100, allow_nan=False), min_size=1, max_size=50))
@settings(max_examples=30)
def test_summarize_count_matches(values: list[float]) -> None:
    stats = summarize(values)
    assert stats.count == len(values)


@given(
    values=st.lists(
        st.floats(min_value=0.1, max_value=100.0, allow_nan=False, allow_infinity=False),
        min_size=2,
        max_size=30,
    )
)
@settings(max_examples=30)
def test_summarize_std_non_negative(values: list[float]) -> None:
    stats = summarize(values)
    assert stats.std >= 0
