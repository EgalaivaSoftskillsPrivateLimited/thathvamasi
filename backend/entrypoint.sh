#!/bin/sh
set -e

echo "⏳ Checking PostgreSQL connection..."
python3 -c "
import time, os, sys
from sqlalchemy import create_engine
from app.core.config import settings

max_retries = 25
for i in range(max_retries):
    try:
        engine = create_engine(settings.DATABASE_URL_SYNC, pool_pre_ping=True)
        with engine.connect() as conn:
            print('✅ PostgreSQL database connection established!')
            sys.exit(0)
    except Exception as e:
        if i == max_retries - 1:
            print(f'⚠️ Warning: Could not connect to PostgreSQL after {max_retries} attempts: {e}')
            print('Continuing startup in offline/resilient mode...')
            sys.exit(0)
        print(f'Waiting for PostgreSQL... ({i+1}/{max_retries})')
        time.sleep(1)
" || true

echo "🔄 Running Alembic database migrations..."
alembic upgrade head || echo "⚠️ Alembic migration skipped or already up to date"

echo "🚀 Starting Uvicorn API server on port ${PORT:-8000}..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
