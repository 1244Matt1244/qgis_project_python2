.PHONY: help install install-dev test test-unit test-integration lint format type-check clean build docs

help:
@echo "Available commands:"
@echo "  install           Install package"
@echo "  install-dev       Install with dev dependencies"
@echo "  test              Run all tests"
@echo "  test-unit         Run unit tests only"
@echo "  test-integration  Run integration tests only"
@echo "  lint              Run ruff linter"
@echo "  format            Format code with ruff"
@echo "  type-check        Run mypy"
@echo "  clean             Clean build artifacts"
@echo "  build             Build wheel and sdist"
@echo "  docs              Serve documentation locally"

install:
pip install -e .

install-dev:
pip install -e ".[dev]"
pre-commit install

test:
pytest

test-unit:
pytest -m unit

test-integration:
pytest -m integration

lint:
ruff check src tests

format:
ruff format src tests
ruff check --fix src tests

type-check:
mypy src

clean:
rm -rf build dist *.egg-info .pytest_cache .ruff_cache .mypy_cache .hypothesis
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

build: clean
python -m build

docs:
mkdocs serve
