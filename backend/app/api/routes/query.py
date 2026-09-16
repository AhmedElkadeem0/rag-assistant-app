from fastapi import APIRouter, HTTPException
from app.schemas.query import QueryRequest, QueryResponse
from app.services.generation import generate_answer

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.post("/query", response_model=QueryResponse)
def query_rag(payload: QueryRequest):
    try:
        answer, sources = generate_answer(payload.question)
        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))