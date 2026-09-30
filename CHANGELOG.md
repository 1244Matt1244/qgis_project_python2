# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-09-30

### Added
- Initial project structure with Clean Architecture layout
- Core modules: `stats`, `vector`, `raster`, `boulder`
- CLI built with Typer and Rich (`boulder analyze`, `raster info`, `vector metrics`)
- Configuration via Pydantic Settings with `.env` support
- Structured logging with structlog
- Custom exception hierarchy
- 30 tests (unit + Hypothesis property-based + CLI integration)
- Docker image with geospatial system dependencies
- GitHub Actions CI (Python 3.11 + 3.12, lint, type-check, test, Docker build)
- Pre-commit hooks (ruff, standard file checks)
