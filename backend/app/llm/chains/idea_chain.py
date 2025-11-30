# backend/app/llm/chains/idea_chain.py

import json
from typing import List
from pydantic import BaseModel, ValidationError

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import RunnableMap

from app.llm.solar_langchain import SolarChatModel


class IdeaCard(BaseModel):
    title: str
    summary: str
    keywords: List[str]
    labels: List[str]
    difficulty: str
    raw_text: str


prompt = ChatPromptTemplate.from_template("""
너는 사용자의 아이디어를 정리하는 Idea Structuring Assistant이다.

아래 규칙을 반드시 지켜라:
1. 출력은 **JSON만** 포함해야 한다. 여는 `{{` 전후에 절대 문구 넣지 말 것.
2. title: 6~12자 사이의 핵심 제목
3. summary: 1~2문장으로 요약
4. keywords: 기술/개념/도메인 키워드 3~7개
5. labels: ["web", "ai", "ocr", "productivity"] 등 유형 태그
6. difficulty: "easy" | "medium" | "hard"

입력 아이디어:
{user_text}

출력(JSON):
{{
  "title": "",
  "summary": "",
  "keywords": [],
  "labels": [],
  "difficulty": ""
}}
""")


class IdeaCreatorChain:

    def __init__(self):
        self.llm = SolarChatModel()
        self.chain = prompt | self.llm

    async def run(self, user_text: str) -> IdeaCard:
        response = await self.chain.ainvoke({"user_text": user_text})

        text = response.content if isinstance(response, AIMessage) else response

        # JSON 파싱 (앞뒤 잡소리 대비)
        try:
            data = json.loads(text)
        except:
            json_str = text[text.find("{"): text.rfind("}") + 1]
            data = json.loads(json_str)

        data["raw_text"] = user_text
        return IdeaCard(**data)