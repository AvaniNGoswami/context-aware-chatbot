from sqlalchemy import Column,String,DateTime
from app.db.base import Base
from datetime import datetime

class Users(Base):
    __tablename__='users'
    id = Column(String,primary_key=True)
    name = Column(String)
    role = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime)