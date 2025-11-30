from app.llm.solar_client import SolarClient
import json

solar = SolarClient()

async def create_idea_card(user_text: str) -> dict:
    system_prompt = """
        너는 사용자의 아이디어를 정리하는 Idea Structuring Assistant이다.
        사용자의 불완전한 설명을 정돈하고, 핵심을 추출해 JSON 형식으로 출력해야 한다.

        다음 규칙을 반드시 지켜라:

        1. 출력은 반드시 유효한 JSON만 포함해야 한다. 추가 문구, 설명 절대 금지.
        2. title은 6~12자 사이로 핵심만 요약.
        3. summary는 1~2문장으로 간단하게 핵심 설명.
        4. keywords는 개념, 기술 스택, 도메인 용어를 3~7개 추출.
        5. labels는 아이디어 유형을 태그로 나타냄. 예: ["web", "ai", "ocr", "productivity"]
        6. difficulty는 "easy" | "medium" | "hard" 중 하나.
        7. 입력이 난잡해도 핵심 의미를 파악해 구조화한다.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"다음 아이디어를 카드로 정리해줘:\n\n{user_text}"}
    ]

    response = await solar.chat(messages)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        # LLM이 잘못된 JSON을 응답했을 때 fallback 처리
        fixed = response[response.find("{"): response.rfind("}") + 1]
        return json.loads(fixed)
