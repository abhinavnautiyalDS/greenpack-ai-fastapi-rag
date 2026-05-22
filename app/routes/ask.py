from fastapi import APIRouter
from app.models.schemas import AskRequest
from app.services.rag_service import RAGService

router = APIRouter()


@router.post("/ask")
def ask_question(payload: AskRequest):

    response = RAGService.ask_question(payload.question)

    return response