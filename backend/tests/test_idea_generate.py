import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_generate_idea_card():
    """아이디어 카드 생성 API 테스트"""

    transport = ASGITransport(app=app)

    sample_input = {"text": "AI로 음악 추천을 개인화하는 아이디어"}

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post("/api/idea/generate", json=sample_input)

    assert r.status_code == 200
    assert "card" in r.json()
    print("Generated Idea Card:", r.json()["card"])

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_generate_idea_card())