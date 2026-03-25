from fastapi import FastAPI
from app.router import register, chat


app = FastAPI(title='welcome to context aware chatbot')

@app.get('/')
def health_check():
    return {'msg':'welcome to context aware chatbot'}

app.include_router(register.router)
app.include_router(chat.router)