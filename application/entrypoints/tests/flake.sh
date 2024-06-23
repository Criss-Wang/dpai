#!/usr/bin/env bash

set -e

pip install --quiet -r requirements.dev.txt
python -m flake8 --max-line-length=88
