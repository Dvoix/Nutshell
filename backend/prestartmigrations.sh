#!/usr/bin/env sh

set -e

echo "Run apply migrations"
uv run --project backend --no-dev alembic -c backend/src/alembic.ini upgrade head
echo "Migrations applied"

exec "$@"
