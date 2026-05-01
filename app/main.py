from fastapi import FastAPI
from app.router import register, chat

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title='welcome to context aware chatbot')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get('/')
def health_check():
    return {'msg':'welcome to context aware chatbot'}

app.include_router(register.router)
app.include_router(chat.router)