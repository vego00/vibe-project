from fastapi import APIRouter
from app.llm.chains.create_idea_card import create_idea_card

router = APIRouter()

@router.post("/generate")
async def generate_idea_card(payload: dict):
    user_input = payload.get("text")
    result = await create_idea_card(user_input)
    return {"card": result}
