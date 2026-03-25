from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from app.db.base import Base

class DistressTracker(Base):
    __tablename__ = "distress_tracker"

    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    streak_count = Column(Integer, default=0)
    last_session_time = Column(DateTime)