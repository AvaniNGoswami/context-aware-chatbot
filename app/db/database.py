from sqlalchemy import create_engine
from app.db.base import Base
from app.core.config import DATABASE_URL
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL,echo=True)

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)