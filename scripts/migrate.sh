#!/usr/bin/env bash

if [ ! -f "./.env" ]; then
  echo "❌ Error: .env file not found in the current directory. Are you running the script from the 'backend' directory?"
  exit 1
fi

source ./.env

if ! source .venv/Scripts/activate; then
  echo "Failed to activate virtual environment"
  exit 1
fi

export PYTHONPATH="$(pwd)"

# 2. Check if we can change to the target directory
TARGET_DIR="database"
if ! cd "$TARGET_DIR"; then
  echo "❌ Error: Failed to change directory to '$TARGET_DIR'. Are you running the script from the 'backend' directory?"
  exit 1
fi

alembic upgrade head