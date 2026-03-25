import requests
import os
from datetime import datetime, timedelta
from app.models.session import Session
import uuid
from app.models.distress_tracker import DistressTracker
from app.models.distress_tracker import DistressTracker

SESSION_MESSAGE_LIMIT = 20
SESSION_TIMEOUT_MIN = 30

GROQ_API = os.getenv("GROQ_API_KEY")

def generate_response(user_message, role_prompt, emotion, session):

    system_prompt = f"""
{role_prompt}

User emotional state: {emotion}

Adapt your tone based on this emotion.
"""

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    MAX_HISTORY = 10

    if session.conversation:
        if session.conversation:
            for msg in session.conversation[-MAX_HISTORY:]:
                messages.append({
                    "role": msg.get("role"),
                    "content": msg.get("content")
                })

    messages.append({
        "role": "user",
        "content": user_message
    })

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": messages,
            "temperature": 0.7
        }
    )

    if response.status_code != 200:
        print("HTTP ERROR:", response.status_code, response.text)
        return "API request failed"

    data = response.json()

    if "error" in data:
        print("GROQ ERROR:", data["error"])
        return "LLM error occurred"

    if "choices" not in data:
        print("UNEXPECTED RESPONSE:", data)
        return "Invalid response format"

    return data["choices"][0]["message"]["content"]



def get_or_create_session(db, user_id):

    session = db.query(Session)\
        .filter(Session.user_id == user_id)\
        .order_by(Session.created_at.desc())\
        .first()

    if session:
        time_diff = datetime.utcnow() - session.start_time

        if (
            session.message_count < SESSION_MESSAGE_LIMIT
            and time_diff < timedelta(minutes=SESSION_TIMEOUT_MIN)
        ):
            return session

    new_session = Session(
        id=str(uuid.uuid4()),
        user_id=user_id,
        message_count=0
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session


def update_session(session, emotion, user_message, bot_response, db):
    session.message_count += 1
    session.total_message_count += 1

    if emotion in ["depressed", "disturbed"]:
        session.distress_message_count += 1

    if session.conversation is None:
        session.conversation = []
    distress_ratio = session.distress_message_count / session.total_message_count
    if distress_ratio >= 0.4:
       session.distress_flag = True
    else:
        session.distress_flag = False

    session.conversation.append({
        "role": "user",
        "content": user_message,
        "emotion": emotion
    })

    session.conversation.append({
        "role": "assistant",
        "content": bot_response
    })

    db.commit()



def update_distress_streak(db, user_id, session):

    if session.message_count < SESSION_MESSAGE_LIMIT:
        return None

    tracker = db.query(DistressTracker)\
        .filter(DistressTracker.user_id == user_id)\
        .first()

    if not tracker:
        tracker = DistressTracker(user_id=user_id, streak_count=0)
        db.add(tracker)

    if session.distress_flag:

        if tracker.last_session_time:
            gap = datetime.utcnow() - tracker.last_session_time

            if gap.total_seconds() <= 86400:  
                tracker.streak_count += 1
            else:
                tracker.streak_count = 1
        else:
            tracker.streak_count = 1
        if tracker.streak_count > 10:
            tracker.streak_count = 1

        tracker.last_session_time = datetime.utcnow()

    else:
        tracker.streak_count = 0

    db.commit()

    return tracker.streak_count
def send_sms(user):
    print(f" 🔥🔥🔥🔥🔥🔥🔥🔥[ALERT] SMS sent to {user.emergency_contact_phone}")


def make_call(user):
    print(f" 🔥🔥🔥🔥🔥🔥🔥🔥[ALERT] Calling {user.emergency_contact_phone}")

def handle_alerts(user, streak_count):

    if not user.consent_for_alerts:
        return

    if streak_count >= 5 and streak_count < 10:
        send_sms(user)

    elif streak_count >= 10:
        make_call(user)