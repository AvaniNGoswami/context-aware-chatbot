from sqlalchemy.orm import Session
from app.models.users import Users

def get_user(db: Session, user_id: str):
    return db.query(Users).filter(Users.id == user_id).first()