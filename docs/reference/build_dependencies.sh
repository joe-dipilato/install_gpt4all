#!/usr/bin/env sh

########################################################################################################################
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -
poetry install
poetry config virtualenvs.in-project true
########################################################################################################################

