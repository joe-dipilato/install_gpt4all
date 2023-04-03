#!/usr/bin/env sh

curl -sSL https://install.python-poetry.org | python3 -
poetry config virtualenvs.in-project true
poetry install