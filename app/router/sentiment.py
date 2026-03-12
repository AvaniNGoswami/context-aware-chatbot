from fastapi import APIRouter
from app.services import nlp_services
from pydantic import BaseModel

class SentimentRequest(BaseModel):
    text: str

router = APIRouter(prefix='/sentiment',tags=['Sentiment Analysis'])

@router.post('/')
def sentiment_analysis(data: SentimentRequest):
    result = nlp_services.analyze(data.text)
    return result