#!/usr/bin/env bash

set -e

pip install --quiet -r requirements.dev.txt
python -m coverage run -m pytest $@
python -m coverage report
