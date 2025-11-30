import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from typing import List, Optional, Any
from pydantic import PrivateAttr

from langchain_core.messages import (
    BaseMessage, AIMessage, HumanMessage, SystemMessage
)
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.outputs import ChatGeneration, ChatResult

from app.llm.solar_client import SolarClient
from app.core.config import settings


class SolarChatModel(BaseChatModel):
    """Solar Pro2 API를 LangChain ChatModel 형식으로 래핑."""

    # 🔥 BaseChatModel은 Pydantic Model → 내부 필드는 반드시 PrivateAttr로 선언
    _client: SolarClient = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._client = SolarClient()

    # ---------------------------------------------------------
    def _convert_messages(self, messages: List[BaseMessage]) -> List[dict]:
        result = []
        for m in messages:
            if isinstance(m, HumanMessage):
                result.append({"role": "user", "content": m.content})
            elif isinstance(m, SystemMessage):
                result.append({"role": "system", "content": m.content})
            elif isinstance(m, AIMessage):
                result.append({"role": "assistant", "content": m.content})
        return result

    # ---------------------------------------------------------
    def _call(self, messages, **kwargs):
        raise NotImplementedError("Use async mode")

    async def _acall(self, messages, **kwargs) -> AIMessage:
        payload = self._convert_messages(messages)
        content = await self._client.chat(payload)
        return AIMessage(content=content)

    # ---------------------------------------------------------
    def _generate(self, messages, **kwargs):
        raise NotImplementedError

    async def _agenerate(self, messages, **kwargs) -> ChatResult:
        msg = await self._acall(messages, **kwargs)
        return ChatResult(generations=[ChatGeneration(message=msg)])

    # ---------------------------------------------------------
    @property
    def _llm_type(self) -> str:
        return settings.SOLAR_MODEL
