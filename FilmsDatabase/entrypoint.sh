#!/bin/bash
set -e

echo "Running migrations to revision: $TARGET_MIGRATION"
alembic upgrade "$TARGET_MIGRATION"


# Execute the command passed to docker run
exec "$@"