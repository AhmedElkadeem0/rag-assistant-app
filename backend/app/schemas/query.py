from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, example="What is microservices architecture?")

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]