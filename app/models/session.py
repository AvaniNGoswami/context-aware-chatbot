# from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey
# from app.db.base import Base
# import datetime

# class Session(Base):
#     __tablename__ = "sessions"

#     id = Column(String, primary_key=True)
#     user_id = Column(String, ForeignKey("users.id"))

#     start_time = Column(DateTime, default=datetime.datetime.utcnow)
#     end_time = Column(DateTime, nullable=True)

#     message_count = Column(Integer, default=0)
#     distress_flag = Column(Boolean, default=False)

#     created_at = Column(DateTime, default=datetime.datetime.utcnow)


from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base
import datetime
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import JSONB

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"))

    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

    message_count = Column(Integer, default=0)
    distress_flag = Column(Boolean, default=False)

    # 🔥 NEW FIELD
    # conversation = Column(JSONB, default=list)
    conversation = Column(MutableList.as_mutable(JSONB), default=list)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)