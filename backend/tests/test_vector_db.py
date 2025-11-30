import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
import asyncio
from sqlalchemy import text
from app.core.db import engine

@pytest.mark.asyncio
async def test_vector_db():
    async with engine.begin() as conn:
        # 1) 테이블 삭제
        await conn.execute(text("DROP TABLE IF EXISTS test_vectors"))

        # 2) 테이블 생성
        await conn.execute(text("""
            CREATE TABLE test_vectors (
                id SERIAL PRIMARY KEY,
                embedding VECTOR(3)
            )
        """))

        # 3) 벡터 삽입
        await conn.execute(text("""
            INSERT INTO test_vectors (embedding)
            VALUES ('[1, 2, 3]')
        """))

        # 4) 벡터 검색
        result = await conn.execute(text("""
            SELECT id, embedding <-> '[1, 2, 4]' AS distance
            FROM test_vectors
        """))

        rows = result.fetchall()
        print("Vector Search Result:", rows)
        # 기대 출력 : Vector Search Result: [(1, 1.0)]

if __name__ == "__main__":
    asyncio.run(test_vector_db())