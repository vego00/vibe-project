import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from app.core.config import settings


@pytest.mark.asyncio
async def test_database_and_vector():
    """PostgreSQL 연결 + pgvector 기능 테스트"""

    engine = create_async_engine(settings.DATABASE_URL, echo=False)

    async with engine.begin() as conn:

        # 1) DB 연결 테스트
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1

        # 2) VECTOR TABLE 생성
        await conn.execute(text("DROP TABLE IF EXISTS test_vectors"))
        await conn.execute(text("""
            CREATE TABLE test_vectors (
                id SERIAL PRIMARY KEY,
                embedding VECTOR(3)
            )
        """))

        # 3) VECTOR INSERT
        await conn.execute(
            text("INSERT INTO test_vectors (embedding) VALUES ('[1,2,3]'::vector)")
        )

        # 4) VECTOR SELECT
        result = await conn.execute(
            text("SELECT embedding FROM test_vectors LIMIT 1")
        )
        row = result.fetchone()
        assert row is not None

        # 5) VECTOR VALUE 체크
        vec = str(row[0]).strip()
        assert vec == "[1,2,3]"

    print("Database + Vector DB tests passed!")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_database_and_vector())