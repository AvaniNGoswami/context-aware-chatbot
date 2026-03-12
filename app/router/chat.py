from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.crud.user import get_user
from app.crud.emotion import update_distress_count
from app.services.emotion_service import detect_emotion
from app.services.chat_service import generate_response
from app.prompts.role_prompts import ROLE_PROMPTS

from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    message: str


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/chat")

def chat(req: ChatRequest, db: Session = Depends(get_db)):

    user = get_user(db, req.user_id)

    if not user:
        return {"error":"user not found"}

    role = user.role

    emotion = detect_emotion(req.message)

    if emotion in ["depressed","disturbed"]:
        update_distress_count(db, req.user_id)

    role_prompt = ROLE_PROMPTS.get(role, ROLE_PROMPTS["default"])

    reply = generate_response(
        req.message,
        role_prompt,
        emotion
    )

    return {
        "emotion": emotion,
        "response": reply
    }