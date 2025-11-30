import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_generate_idea_card_async():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "text": "멀티모달 기반으로 사진에서 문제를 추출하고 아이디어를 자동 생성해주는 서비스"
        }
        response = await ac.post("/api/idea/generate", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "card" in data
    card = data["card"]

    assert isinstance(card, dict)
    assert "title" in card
    assert "summary" in card
    assert "keywords" in card
    assert "labels" in card
    assert "difficulty" in card

    print("\n✓ Async test passed. Response:")
    print(data)
