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

    # 🔹 1. Get user
    user = get_user(db, req.user_id)
    if not user:
        return {"error": "user not found"}

    # 🔹 2. Session
    session = get_or_create_session(db, req.user_id)

    # 🔹 3. Role prompt (🔥 MOVE THIS UP)
    role_prompt = ROLE_PROMPTS.get(user.role, ROLE_PROMPTS["default"])

    # 🔹 4. Emotion
    emotion = detect_emotion(req.message)

    # 🔹 5. Generate response (ONLY ONCE)
    reply = generate_response(
        req.message,
        role_prompt,
        emotion,
        session   # 🔥 don’t forget this
    )

    # 🔹 6. Update session
    update_session(session, emotion, req.message, reply, db)
    print("SESSION JSON:", session.conversation)

    # 🔹 7. Update streak
    streak = update_distress_streak(db, req.user_id, session)

    # 🔹 8. Alerts
    if streak:
        handle_alerts(user, streak)

    # 🔹 9. Save chat
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