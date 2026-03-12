# import requests
# import os

# GROK_API = os.getenv("GROQ_API_KEY")

# def detect_emotion(text: str):

#     prompt = f"""
#     Classify emotion of this text.

#     Return only one label:
#     happy, neutral, sad, angry, depressed, disturbed

#     Text:
#     {text}
#     """

#     response = requests.post(
#         "https://api.x.ai/v1/chat/completions",
#         headers={
#             "Authorization": f"Bearer {GROK_API}",
#             "Content-Type": "application/json"
#         },
#         json={
#             "model": "grok-4-fast-reasoning",
#             "messages":[
#                 {"role":"user","content":prompt}
#             ]
#         }
#     )


#     print("🔥🔥🔥🔥🔥STATUS:", response.status_code)
#     print("🔥🔥🔥🔥🔥RESPONSE:", response.text)

#     if response.status_code != 200:
#         return "neutral"

#     result = response.json()

#     emotion = result["choices"][0]["message"]["content"].strip()

#     return emotion.lower()



import requests
import os

GROQ_API = os.getenv("GROQ_API_KEY")

def detect_emotion(text: str):

    prompt = f"""
Classify the emotion of this text.

Return ONLY one word from:
happy, neutral, sad, angry, depressed, disturbed

Text:
{text}
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages":[
                {"role":"system","content":"You are an emotion classifier."},
                {"role":"user","content":prompt}
            ],
            "temperature":0
        }
    )

    print("🔥🔥🔥🔥🔥STATUS:", response.status_code)
    print("🔥🔥🔥🔥RESPONSE:", response.text)

    data = response.json()

    if "choices" not in data:
        return "neutral"

    emotion = data["choices"][0]["message"]["content"].strip()

    return emotion.lower()