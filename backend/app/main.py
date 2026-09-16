from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import query
from app.services.retrieval import rag_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load embedding model & vector store globally at startup
    rag_service.initialize()
    yield

app = FastAPI(title="RAG Document Assistant API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router)