import asyncio
from sqlalchemy import text
from app.core.db import engine

async def test_conn():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("DB 연결 성공:", result.scalar())
    except Exception as e:
        print("DB 연결 실패:", e)

asyncio.run(test_conn())
