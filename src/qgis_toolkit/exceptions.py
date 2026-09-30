"""Custom exceptions for qgis-toolkit."""


class QgisToolkitError(Exception):
    """Base exception for all qgis-toolkit errors."""


class GeometryError(QgisToolkitError):
    """Raised when a geometry is invalid or cannot be processed."""


class RasterError(QgisToolkitError):
    """Raised when raster operations fail."""


class ValidationError(QgisToolkitError):
    """Raised when input validation fails."""


class ProcessingError(QgisToolkitError):
    """Raised when a processing operation fails."""
