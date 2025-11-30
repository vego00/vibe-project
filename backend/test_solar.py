import asyncio
import httpx
from app.core.config import settings

async def test_solar():
    headers = {
        "Authorization": f"Bearer {settings.SOLAR_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.SOLAR_MODEL,
        "messages": [
            {"role": "user", "content": "안녕, 너 연결 테스트 중이야. 한 문장으로 응답해줘."}
        ],
        "max_tokens": 50,
    }

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(settings.SOLAR_API_URL, headers=headers, json=payload)

    print("Status:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    asyncio.run(test_solar())
