#!/usr/bin/env bash

set -o errexit

echo "Installing dependencies..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Running migrations..."
export PYTHONPATH="$(pwd)"

cd database
alembic upgrade head

echo "Build complete!"