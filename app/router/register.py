from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db.database import engine
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
from app.models.users import Users

class register(BaseModel):
    name:str
    role:str
    email:str
    password:str

router = APIRouter(prefix='/register',tags=['Register'])

@router.post('/')
def registration(data:register):
    with Session(engine) as session:
        user = Users(
            id = str(uuid4()),
            name = data.name,
            role = data.role,
            email = data.email,
            password = data.password,
            created_at = datetime.utcnow()
        )
        session.add(user)
        session.commit()
        session.refresh(user)
    return {'status':'recorded details'}



