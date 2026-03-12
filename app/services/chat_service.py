# import os
# import requests

# GROK_API = os.getenv("GROK_API_KEY")

# def generate_response(user_message, role_prompt, emotion):

#     system_prompt = f"""
#     {role_prompt}

#     User emotional state: {emotion}

#     Adapt tone accordingly.
#     """

#     response = requests.post(
#         "https://api.x.ai/v1/chat/completions",
#         headers={
#             "Authorization": f"Bearer {GROK_API}",
#             "Content-Type": "application/json"
#         },
#         json={
#             "model":"grok-2-latest",
#             "messages":[
#                 {"role":"system","content":system_prompt},
#                 {"role":"user","content":user_message}
#             ]
#         }
#     )

#     data = response.json()

#     return data["choices"][0]["message"]["content"]

import requests
import os

GROQ_API = os.getenv("GROQ_API_KEY")

def generate_response(user_message, role_prompt, emotion):

    system_prompt = f"""
{role_prompt}

User emotional state: {emotion}

Adapt your tone based on this emotion.
"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API}",
            "Content-Type": "application/json"
        },
        json={
            "model":"llama-3.1-8b-instant",
            "messages":[
                {"role":"system","content":system_prompt},
                {"role":"user","content":user_message}
            ],
            "temperature":0.7
        }
    )

    data = response.json()

    if "choices" not in data:
        return "Sorry, I couldn't process that."

    return data["choices"][0]["message"]["content"]