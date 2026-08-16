#!/usr/bin/env bash

if [ -z "$1" ]; then
  echo "❌ Error: Migration name not provided."
  echo "💡 Usage: $0 <migration_name>"
  echo "   Example: $0 add_users_table"
  exit 1
fi

MIGRATION_NAME="$1"

if [ ! -f "./.env" ]; then
  echo "❌ Error: .env file not found in the current directory. Are you running the script from the 'backend-v2' directory?"
  exit 1
fi

source ./.env

if ! source .venv/Scripts/activate; then
  echo "Failed to activate virtual environment"
  exit 1
fi

export PYTHONPATH="$(pwd)"

TARGET_DIR="database"
if ! cd "$TARGET_DIR"; then
  echo "❌ Error: Failed to change directory to '$TARGET_DIR'. Are you running the script from the 'backend-v2' directory?"
  exit 1
fi

echo "⚙️ Generating migration: '$MIGRATION_NAME'..."

if ! alembic revision --autogenerate -m "$MIGRATION_NAME"; then
  echo "❌ Error: Migration generation failed (Alembic returned an error)."
  exit 1
fi

echo "✅ Success! Migration files have been created."
echo "💡 Run scripts/migrate.sh to apply these migrations to the database."
