from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from services.ai_agent import ai_service
from dependencies import get_current_user
from models import User

router = APIRouter(prefix="/api/ai", tags=["AI"])

class DuckRequest(BaseModel):
    problem_description: str
    user_code: str
    language: str

@router.post("/duck")
async def ask_rubber_duck(req: DuckRequest, current_user: User = Depends(get_current_user)):
    """
    请求 AI 小黄鸭对 WA 代码提供启发式建议
    """
    hint = await ai_service.get_rubber_duck_hint(
        problem_description=req.problem_description,
        user_code=req.user_code,
        language=req.language
    )
    return {"hint": hint}
