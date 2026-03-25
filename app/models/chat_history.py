from sqlalchemy import Column, ForeignKey, String, DateTime, Text
from datetime import datetime
from app.db.base import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(String, primary_key=True)
    user_id = Column(String)
    user_message = Column(Text)
    detected_emotion = Column(String)
    bot_response = Column(Text)
    session_id = Column(String, ForeignKey("sessions.id"))
    role = Column(String)  
    created_at = Column(DateTime, default=datetime.utcnow)