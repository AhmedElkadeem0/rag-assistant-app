"""Test the complete retrieval and generation pipeline."""

from typing import Any, Dict, List

from backend.app.services.context_selector import ContextSelector
from backend.app.services.generation import GenerationService
from backend.app.services.retrieval import RetrievalService


TOP_K = 10
MODEL_NAME = "qwen2.5:1.5b"


def print_sources(chunks: List[Dict[str, Any]]) -> None:
    """Print retrieved or selected sources."""
    print("CONTEXT SENT TO LLM")
    print("-" * 80)

    for index, chunk in enumerate(chunks, start=1):
        metadata = chunk["metadata"]

        chunk_id = metadata.get(
            "chunk_id",
            f"chunk-{index}",
        )

        content_type = metadata.get(
            "content_type",
            "Unknown",
        )

        section = metadata.get(
            "section",
            "Unknown",
        )

        distance = chunk.get(
            "distance",
            float("inf"),
        )

        print(
            f"[{index}] {chunk_id} | "
            f"section={section} | "
            f"type={content_type} | "
            f"distance={distance:.4f}"
        )


def main() -> None:
    """Run end-to-end retrieval and generation tests."""
    questions = [
        "What is HTTPS?",
        "How does the TLS handshake work?",
        "What are the authentication factors?",
        "Give examples of two-factor authentication.",
        "What is Defense in Depth?",
        "What are the three authentication factors mentioned in the lesson",
    ]

    retrieval_service = RetrievalService(
        top_k=TOP_K,
    )

    context_selector = ContextSelector()

    generation_service = GenerationService(
        model_name=MODEL_NAME,
    )

    for question in questions:
        print("\n" + "=" * 80)
        print(f"QUESTION: {question}")
        print("=" * 80)

        retrieved_chunks = retrieval_service.retrieve(
            question,
        )

        print_sources(retrieved_chunks)

        selected_chunks = context_selector.select(
            question,
            retrieved_chunks,
        )

        print()
        print_sources(selected_chunks)

        answer = generation_service.generate(
            question,
            selected_chunks,
        )

        print("\nANSWER")
        print("-" * 80)
        print(answer)


if __name__ == "__main__":
    main()