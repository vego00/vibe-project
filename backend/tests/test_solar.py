# backend/tests/test_solar.py

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest
from httpx import AsyncClient, ASGITransport

from app.core.config import settings
from app.llm.solar_client import SolarClient
from app.llm.solar_langchain import SolarChatModel
from app.llm.chains.idea_chain import IdeaCreatorChain
from app.main import app


# ---------------------------------------------------------
# 1) Solar API 실제 호출 테스트
# ---------------------------------------------------------
# @pytest.mark.asyncio
@pytest.mark.skip(reason="External API call skipped during tests")
async def test_solar_api_reachable():
    """Solar Pro2 API 실제 호출 테스트"""
    pass

    payload = {
        "model": settings.SOLAR_MODEL,
        "messages": [{"role": "user", "content": "테스트 메시지입니다."}],
        "max_tokens": 20,
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
        assert "content" in data["choices"][0]["message"]
        print("Solar API Response:", data["choices"][0]["message"]["content"])
    else:
        print("Solar API Error:", r.status_code, r.text)


# ---------------------------------------------------------
# 2) SolarClient.chat 단위 테스트 (mock 없음 = 실제 Solar 호출)
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_solar_client_chat():
    """SolarClient.chat 직접 호출 테스트"""
    client = SolarClient()

    response = await client.chat(
        [{"role": "user", "content": "안녕? 한줄로 대답해줘"}],
        max_tokens=20
    )

    assert isinstance(response, str)
    assert len(response) > 0
    print("SolarClient Response:", response)


# ---------------------------------------------------------
# 3) SolarChatModel 테스트
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_solar_chat_model():
    """LangChain 래퍼(SolarChatModel) 테스트"""
    model = SolarChatModel()

    from langchain_core.messages import HumanMessage
    result = await model._acall([
        # LangChain BaseMessage로 입력
        # 아래가 HumanMessage 객체로 변환됨
        HumanMessage(content="한 문장으로 대답해줘")
    ])

    assert result.content
    print("SolarChatModel Output:", result.content)


# ---------------------------------------------------------
# 4) IdeaCreatorChain 테스트 (아이디어 → IdeaCard)
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_idea_creator_chain():
    """새로운 아이디어 파이프라인(LangChain 기반) 테스트"""

    chain = IdeaCreatorChain()

    result = await chain.run("AI로 개인 맞춤 추천 기능을 만들고 싶어")

    assert result.title
    assert result.difficulty in ["easy", "medium", "hard"]
    print("IdeaCard:", result.model_dump())


# ---------------------------------------------------------
# 5) FastAPI 엔드포인트 테스트 (/api/idea/generate)
# ---------------------------------------------------------
@pytest.mark.asyncio
async def test_api_generate_idea_card():
    """FastAPI 기반 아이디어 카드 생성 API 테스트"""

    transport = ASGITransport(app=app)
    input_data = {"text": "음악 취향 분석하는 AI 아이디어"}

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        r = await ac.post("/api/idea/generate", json=input_data)

    assert r.status_code == 200
    body = r.json()
    assert "card" in body
    print("Generated IdeaCard via API:", body["card"])
