from sqlalchemy import Column,String,DateTime, Integer, Boolean
from app.db.base import Base
from datetime import datetime

class Users(Base):
    __tablename__='users'
    id = Column(String,primary_key=True)
    name = Column(String)
    role = Column(String)
    email = Column(String)
    password = Column(String)
    emergency_contact_name = Column(String)
    emergency_contact_phone = Column(String)   
    user_phone = Column(String)                
    consent_for_alerts = Column(Boolean, default=False)

    created_at = Column(DateTime)