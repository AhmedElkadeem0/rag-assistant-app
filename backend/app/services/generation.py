import ollama
from app.core.config import settings
from app.services.retrieval import rag_service

def generate_answer(query: str) -> tuple[str, list[str]]:
    chunks, sources = rag_service.retrieve(query)
    context_str = "\n\n".join([f"[Source: {src}]\n{txt}" for txt, src in zip(chunks, sources)])
    
    prompt = f"""You are a helpful assistant. Answer the user question based ONLY on the provided context below.
If the answer cannot be found in the context, respond with "I cannot find this information in the documents."

Context:
{context_str}

Question: {query}
Answer:"""

    response = ollama.chat(
        model=settings.LLM_MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["message"]["content"], sources