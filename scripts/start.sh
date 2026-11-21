
#!/bin/sh
set -eu

echo "Starting MovieRec FastAPI..."

exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000
