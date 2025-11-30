import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
import asyncio
from sqlalchemy import text
from app.core.db import engine

@pytest.mark.asyncio
async def test_conn():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("DB 연결 성공:", result.scalar())
    except Exception as e:
        print("DB 연결 실패:", e)

if __name__ == "__main__":
    asyncio.run(test_conn())