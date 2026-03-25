from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.crud.user import get_user
from app.crud.emotion import update_distress_count
from app.services.emotion_service import detect_emotion
from app.services.chat_service import generate_response
from app.prompts.role_prompts import ROLE_PROMPTS
from app.crud.chat_history import save_chat

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


from app.services.chat_service import (
    generate_response,
    get_or_create_session,
    update_session,
    update_distress_streak,
    handle_alerts
)


@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):

    user = get_user(db, req.user_id)
    if not user:
        return {"error": "user not found"}

    session = get_or_create_session(db, req.user_id)

    role_prompt = ROLE_PROMPTS.get(user.role, ROLE_PROMPTS["default"])

    emotion = detect_emotion(req.message)

    reply = generate_response(
        req.message,
        role_prompt,
        emotion,
        session   
    )

    update_session(session, emotion, req.message, reply, db)
    print("SESSION JSON:", session.conversation)

    streak = update_distress_streak(db, req.user_id, session)

    if streak:
        handle_alerts(user, streak)

    save_chat(
        db,
        user_id=req.user_id,
        session_id=session.id,
        user_message=req.message,
        emotion=emotion,
        bot_response=reply
    )

    return {
        "emotion": emotion,
        "response": reply,
        "session_id": session.id,
        "streak": streak
    }