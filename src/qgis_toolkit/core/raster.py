"""Raster operations using rasterio."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import rasterio
from rasterio.mask import mask as rio_mask
from shapely.geometry import Polygon, mapping

from qgis_toolkit.exceptions import RasterError, ValidationError


@dataclass(frozen=True)
class RasterInfo:
    """Metadata for a raster."""

    width: int
    height: int
    count: int
    crs: str
    transform: tuple[float, ...]
    nodata: float | None
    dtype: str
    bounds: tuple[float, float, float, float]
    resolution: tuple[float, float]


@dataclass(frozen=True)
class RasterStats:
    """Statistics computed from raster pixels within a polygon."""

    count: int
    min: float
    max: float
    mean: float
    std: float
    height_range: float


def read_raster_info(path: str | Path) -> RasterInfo:
    """Read raster metadata without loading full data.

    Args:
        path: Path to raster file.

    Returns:
        RasterInfo.

    Raises:
        RasterError: If raster cannot be opened.
    """
    try:
        with rasterio.open(path) as src:
            return RasterInfo(
                width=src.width,
                height=src.height,
                count=src.count,
                crs=str(src.crs) if src.crs else "",
                transform=tuple(src.transform),
                nodata=src.nodata,
                dtype=str(src.dtypes[0]),
                bounds=tuple(src.bounds),
                resolution=(src.res[0], src.res[1]),
            )
    except rasterio.errors.RasterioIOError as e:
        raise RasterError(f"Cannot open raster {path}: {e}") from e


def sample_raster_in_polygon(
    raster_path: str | Path,
    polygon: Polygon,
    band: int = 1,
    all_touched: bool = False,
) -> np.ndarray:
    """Sample raster values within a polygon mask.

    Args:
        raster_path: Path to raster.
        polygon: Shapely polygon in same CRS as raster.
        band: Band index (1-based).
        all_touched: If True, include pixels touching the boundary.

    Returns:
        Flattened array of pixel values (NaN excluded).

    Raises:
        RasterError: If sampling fails.
        ValidationError: If band is invalid.
    """
    if band < 1:
        raise ValidationError(f"Band must be >= 1, got {band}")

    try:
        with rasterio.open(raster_path) as src:
            if band > src.count:
                raise ValidationError(f"Band {band} > raster band count {src.count}")

            geom = [mapping(polygon)]
            out_image, _ = rio_mask(
                src,
                geom,
                crop=True,
                filled=True,
                all_touched=all_touched,
                nodata=src.nodata,
            )
            band_data = out_image[band - 1].astype(float)

            if src.nodata is not None:
                band_data = band_data[band_data != src.nodata]

            band_data = band_data[~np.isnan(band_data)]
            return band_data
    except rasterio.errors.RasterioIOError as e:
        raise RasterError(f"Raster sampling failed: {e}") from e


def compute_raster_stats(
    raster_path: str | Path,
    polygon: Polygon,
    band: int = 1,
    all_touched: bool = False,
) -> RasterStats:
    """Compute statistics from raster values within a polygon.

    Args:
        raster_path: Path to raster.
        polygon: Shapely polygon.
        band: Band index (1-based).
        all_touched: Include boundary pixels.

    Returns:
        RasterStats.

    Raises:
        RasterError: If no valid pixels found.
    """
    values = sample_raster_in_polygon(raster_path, polygon, band, all_touched)

    if values.size == 0:
        raise RasterError("No valid pixels found in polygon")

    min_v = float(np.min(values))
    max_v = float(np.max(values))

    return RasterStats(
        count=int(values.size),
        min=min_v,
        max=max_v,
        mean=float(np.mean(values)),
        std=float(np.std(values, ddof=1)) if values.size > 1 else 0.0,
        height_range=abs(max_v - min_v),
    )
