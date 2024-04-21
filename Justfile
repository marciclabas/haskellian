mod core "packages/haskellian-core/Justfile"
mod iterables "packages/haskellian-iterables/Justfile"
mod either "packages/haskellian-either/Justfile"
mod asyn "packages/haskellian-asyn/Justfile"
mod asyn-iter "packages/haskellian-asyn-iter/Justfile"VENV := ".venv"
PYTHON := ".venv/bin/python"

init:
  rm -drf {{VENV}} || :
  python3.11 -m venv {{VENV}}
  {{PYTHON}} -m pip install --upgrade pip
  {{PYTHON}} -m pip install -r requirements.txt