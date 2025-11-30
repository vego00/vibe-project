import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from httpx import AsyncClient, ASGITransport
from app.core.config import settings
from app.main import app

@pytest.mark.asyncio
async def test_solar_api():
    """Solar Pro2 API 호출 테스트"""

    payload = {
        "model": settings.SOLAR_MODEL,
        "messages": [
            {"role": "user", "content": "테스트 메시지입니다."}
        ],
        "max_tokens": 20
    }

    headers = {
        "Authorization": f"Bearer {settings.SOLAR_API_KEY}",
        "Content-Type": "application/json"
    }

    async with AsyncClient() as ac:
        r = await ac.post(settings.SOLAR_API_URL, json=payload, headers=headers)

    assert r.status_code in [200, 400, 401]
    if r.status_code == 200:
        data = r.json()
        assert "choices" in data
        assert len(data["choices"]) > 0
        assert "message" in data["choices"][0]
        assert "content" in data["choices"][0]["message"]
        print("Solar API Response:", data["choices"][0]["message"]["content"])
    else:
        print(f"Solar API returned status code {r.status_code}: {r.text}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_solar_api())