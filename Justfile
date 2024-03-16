VENV := ".venv"
PYTHON := VENV + "/bin/python"
PKG := "."

default:
  @just --list

# Create venv and install requirements
init:
  rm -drf {{VENV}} || :
  python3.11 -m venv {{VENV}}
  {{PYTHON}} -m pip install --upgrade pip
  {{PYTHON}} -m pip install build twine -r requirements.txt

# Run pytest
test:
  {{PYTHON}} -m pytest

# Build the package (into `dist/`)
build:
  rm -drf {{PKG}}/dist
  cd {{PKG}} && {{PYTHON}} -m build
  rm -drf {{PKG}}/build

# Publish `dist/*` to pypi
publish:
  {{PYTHON}} -m twine upload {{PKG}}/dist/*