from sqlalchemy.orm import Session
from app.models.emotion_counter import EmotionCounter

def update_distress_count(db: Session, user_id: str):

    record = db.query(EmotionCounter).filter(
        EmotionCounter.user_id == user_id
    ).first()

    if not record:
        record = EmotionCounter(
            user_id=user_id,
            distress_count=1
        )
        db.add(record)

    else:
        record.distress_count += 1

    db.commit()