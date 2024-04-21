VENV := justfile_directory() + "/.venv"
PYTHON := justfile_directory() + "/.venv/bin/python"
PKG :=  "haskellian"

help:
  @just --list

# Build the package (into `dist/`)
build:
  cd {{PKG}} && \
  rm -drf dist && \
  {{PYTHON}} -m build && \
  rm -drf build

# Publish `dist/*` to pypi, then delete
publish:
  cp README.md {{PKG}}
  cd {{PKG}} && \
  {{PYTHON}} -m twine upload dist/* && \
  rm -drf dist

# Increase patch version
patch:
  $BUMP pyproject.toml

# Build and publish
republish: patch build publish

# Create venv and install requirements
init:
  rm -drf {{VENV}} || :
  python3.11 -m venv {{VENV}}
  {{PYTHON}} -m pip install --upgrade pip
  {{PYTHON}} -m pip install build twine pytest

# Run pytest
test:
  {{PYTHON}} -m pytest