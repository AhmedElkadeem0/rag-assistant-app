import chromadb
from sentence_transformers import SentenceTransformer
from app.core.config import settings

class RAGService:
    def __init__(self):
        self.embed_model = None
        self.collection = None

    def initialize(self):
        self.embed_model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        chroma_client = chromadb.PersistentClient(path=settings.VECTOR_STORE_DIR)
        self.collection = chroma_client.get_collection(name="tech_docs")

    def retrieve(self, query: str, top_k: int = 2):
        query_embedding = self.embed_model.encode([query]).tolist()
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )
        chunks = results["documents"][0] if results["documents"] else []
        sources = [meta["source"] for meta in results["metadatas"][0]] if results["metadatas"] else []
        return chunks, list(set(sources))

rag_service = RAGService()