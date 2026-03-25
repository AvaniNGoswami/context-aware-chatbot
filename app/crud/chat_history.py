import uuid
from sqlalchemy.orm import Session
from app.models.chat_history import ChatHistory


# def save_chat(
#     db: Session,
#     user_id: str,
#     user_message: str,
#     emotion: str,
#     bot_response: str
# ):

#     chat = ChatHistory(
#         id=str(uuid.uuid4()),
#         user_id=user_id,
#         user_message=user_message,
#         detected_emotion=emotion,
#         bot_response=bot_response
#     )

#     db.add(chat)
#     db.commit()
#     db.refresh(chat)

#     return chat

def save_chat(db, user_id, session_id, user_message, emotion, bot_response):

    chat = ChatHistory(
        id=str(uuid.uuid4()),
        user_id=user_id,
        session_id=session_id,
        user_message=user_message,
        detected_emotion=emotion,
        bot_response=bot_response
    )

    db.add(chat)
    db.commit()