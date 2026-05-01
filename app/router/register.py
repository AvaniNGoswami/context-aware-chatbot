from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db.database import engine
from pydantic import BaseModel
from uuid import uuid4
from datetime import datetime
from app.models.users import Users

# class register(BaseModel):
#     name:str
#     role:str
#     email:str
#     password:str
#     emergency_contact_name : str
#     emergency_contact_phone : str
#     user_phone : str
#     consent_for_alerts : str

class register(BaseModel):
    name: str
    role: str
    email: str
    password: str
    emergency_contact_name: str
    emergency_contact_phone: str
    phone: str   # ✅ match frontend
    consent_for_alerts: bool   # ✅ correct type




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
            created_at = datetime.utcnow(),
            emergency_contact_name = data.emergency_contact_name,
            emergency_contact_phone = data.emergency_contact_phone,
            user_phone = data.phone,
            consent_for_alerts = data.consent_for_alerts

        )
        session.add(user)
        session.commit()
        session.refresh(user)
    return {
    "message": "User registered successfully",
    "user_id": user.id
}



