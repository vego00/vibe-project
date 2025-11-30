import httpx
from app.core.config import settings
from app.utils.retry import async_retry

class SolarClient:

    def __init__(self):
        self.api_key = settings.SOLAR_API_KEY
        self.url = settings.SOLAR_API_URL
        self.model = settings.SOLAR_MODEL

    @async_retry(retries=3, delay=1)
    async def chat(self, messages: list[dict], max_tokens=512, temperature=0.7):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        async with httpx.AsyncClient(timeout=20) as client:
            res = await client.post(self.url, headers=headers, json=payload)

        if res.status_code != 200:
            raise Exception(f"Solar API Error: {res.text}")

        return res.json()["choices"][0]["message"]["content"]
