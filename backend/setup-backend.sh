#!/bin/bash

# 백엔드 초기화
echo "Initializing backend project..."
poetry init --no-interaction \
  --name="vibe-project-backend" \
  --description="AI-powered idea management and auto planning system backend." \
  --author="vego00 <khmute@gmail.com>" \
  --python=">=3.11" \
  --dependency=fastapi \
  --dependency=uvicorn \
  --dependency=pydantic-settings \
  --dependency=sqlalchemy \
  --dependency=asyncpg \
  --dependency=psycopg[binary]

# 개발용 의존성 추가
echo "Adding development dependencies..."
poetry add --group dev black ruff isort pytest httpx

echo "Backend environment setup complete!"
