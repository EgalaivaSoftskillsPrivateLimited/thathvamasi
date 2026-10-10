#!/bin/sh
set -e

PORT="${PORT:-8000}"

echo "⏳ Checking PostgreSQL connection..."
python3 -c "
import time, os, sys
from sqlalchemy import create_engine
from app.core.config import settings

max_retries = 3
for i in range(max_retries):
    try:
        engine = create_engine(settings.DATABASE_URL_SYNC, pool_pre_ping=True)
        with engine.connect() as conn:
            print('✅ PostgreSQL database connection established!')
            sys.exit(0)
    except Exception as e:
        if i == max_retries - 1:
            print(f'⚠️ Notice: PostgreSQL not ready within {max_retries}s: {e}')
            print('Starting FastAPI in resilient mode...')
            sys.exit(0)
        time.sleep(1)
" || true

echo "🔄 Running database migrations..."
alembic upgrade head 2>/dev/null || echo "⚠️ Alembic migration deferred or already up to date"

echo "🚀 Starting Uvicorn API server on port ${PORT}..."
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT}"
