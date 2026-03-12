from sqlalchemy import Column,String,Integer
from app.db.base import Base

class EmotionCounter(Base):
    __tablename__ = "emotion_counter"

    user_id = Column(String, primary_key=True)
    distress_count = Column(Integer, default=0)