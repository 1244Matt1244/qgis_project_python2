"""Integration tests for the CLI."""

from typer.testing import CliRunner

from qgis_toolkit.__version__ import __version__
from qgis_toolkit.cli.main import app

pytestmark = []

runner = CliRunner()


def test_version_command() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_help_shows_commands() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "boulder" in result.stdout
    assert "raster" in result.stdout
    assert "vector" in result.stdout


def test_vector_metrics_square() -> None:
    wkt = "POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0))"
    result = runner.invoke(app, ["vector", "metrics", "--polygon", wkt])
    assert result.exit_code == 0
    assert "Area" in result.stdout
    assert "1.0000" in result.stdout


def test_vector_metrics_invalid_wkt() -> None:
    result = runner.invoke(app, ["vector", "metrics", "--polygon", "not-wkt"])
    assert result.exit_code == 1
    assert "Invalid WKT" in result.stdout
