"""Answer service for the ICT RAG assistant."""

from typing import Any, Dict, List

import ollama


MODEL_NAME = "qwen2.5:3b"

INSUFFICIENT_CONTEXT_MESSAGE = (
    "I don't have enough information in the lesson to answer "
    "this question reliably."
)

LOW_VALUE_CONTENT_TYPES = {
    "question",
    "exercise",
}

EXPLANATORY_CONTENT_TYPES = {
    "concept",
    "process",
    "summary",
    "example",
}


class AnswerService:
    """
    Produce answers from retrieved educational evidence.

    Retrieved evidence is treated as the source of truth.
    Direct evidence is returned without LLM rewriting whenever
    possible. Ollama is reserved for optional synthesis when
    explicitly enabled.
    """

    def __init__(
        self,
        model_name: str = MODEL_NAME,
        use_llm: bool = False,
    ) -> None:
        """Initialize the answer service."""
        self.model_name = model_name
        self.use_llm = use_llm

    @staticmethod
    def _get_text(
        chunk: Dict[str, Any],
    ) -> str:
        """Return chunk text safely."""
        return str(
            chunk.get(
                "text",
                "",
            )
        ).strip()

    @staticmethod
    def _get_metadata(
        chunk: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Return chunk metadata safely."""
        metadata = chunk.get(
            "metadata",
            {},
        )

        if not isinstance(metadata, dict):
            return {}

        return metadata

    @classmethod
    def _get_content_type(
        cls,
        chunk: Dict[str, Any],
    ) -> str:
        """Return a chunk's content type."""
        metadata = cls._get_metadata(chunk)

        return str(
            metadata.get(
                "content_type",
                "",
            )
        )

    @classmethod
    def _get_chunk_id(
        cls,
        chunk: Dict[str, Any],
    ) -> str:
        """Return a chunk identifier safely."""
        metadata = cls._get_metadata(chunk)

        return str(
            metadata.get(
                "chunk_id",
                "",
            )
        )

    @classmethod
    def _has_explanatory_evidence(
        cls,
        chunks: List[Dict[str, Any]],
    ) -> bool:
        """Check whether the evidence contains explanatory content."""
        return any(
            cls._get_content_type(chunk)
            in EXPLANATORY_CONTENT_TYPES
            and bool(cls._get_text(chunk))
            for chunk in chunks
        )

    @classmethod
    def _filter_low_value_chunks(
        cls,
        chunks: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Remove question/exercise chunks when explanatory evidence
        is already available.
        """
        if not chunks:
            return []

        if not cls._has_explanatory_evidence(chunks):
            return chunks

        filtered = [
            chunk
            for chunk in chunks
            if cls._get_content_type(chunk)
            not in LOW_VALUE_CONTENT_TYPES
            and bool(cls._get_text(chunk))
        ]

        return filtered or chunks

    @classmethod
    def _is_single_direct_answer(
        cls,
        chunks: List[Dict[str, Any]],
    ) -> bool:
        """Determine whether one chunk can answer the question directly."""
        if len(chunks) != 1:
            return False

        chunk = chunks[0]

        return (
            cls._get_content_type(chunk)
            in EXPLANATORY_CONTENT_TYPES
            and bool(cls._get_text(chunk))
        )

    @classmethod
    def _build_extractive_answer(
        cls,
        chunks: List[Dict[str, Any]],
    ) -> str:
        """
        Build an answer directly from source evidence.

        No new information is generated here. This is intentionally
        extractive to prevent the language model from introducing
        unsupported facts.
        """
        usable_chunks = cls._filter_low_value_chunks(chunks)

        texts: List[str] = []

        for chunk in usable_chunks:
            text = cls._get_text(chunk)

            if text and text not in texts:
                texts.append(text)

        if not texts:
            return INSUFFICIENT_CONTEXT_MESSAGE

        return "\n\n".join(texts)

    @classmethod
    def _build_context(
        cls,
        chunks: List[Dict[str, Any]],
    ) -> str:
        """Build a numbered evidence context for optional LLM synthesis."""
        context_parts: List[str] = []

        for index, chunk in enumerate(chunks, start=1):
            text = cls._get_text(chunk)

            if not text:
                continue

            metadata = cls._get_metadata(chunk)

            chunk_id = cls._get_chunk_id(chunk)

            section_title = str(
                metadata.get(
                    "section_title",
                    "",
                )
            )

            content_type = cls._get_content_type(
                chunk
            )

            context_parts.append(
                f"[Evidence {index}]\n"
                f"Chunk ID: {chunk_id}\n"
                f"Section: {section_title}\n"
                f"Type: {content_type}\n"
                f"Content:\n{text}"
            )

        return "\n\n".join(context_parts)

    @classmethod
    def _build_synthesis_prompt(
        cls,
        question: str,
        chunks: List[Dict[str, Any]],
    ) -> str:
        """Build a conservative synthesis prompt."""
        context = cls._build_context(chunks)

        return f"""
You are an ICT study assistant.

Answer the student's question using ONLY the evidence below.

The evidence is the ONLY source of truth.

Rules:

1. Do not use outside knowledge.
2. Do not add facts that are not explicitly present.
3. Do not expand acronyms unless the expansion appears in the evidence.
4. Do not invent examples.
5. Do not introduce technical details that are not in the evidence.
6. Do not infer missing information.
7. If the evidence does not support an important part of the answer,
   leave that part out.
8. If the evidence is insufficient to answer the question,
   respond exactly with:

"{INSUFFICIENT_CONTEXT_MESSAGE}"

9. Preserve the terminology and meaning of the evidence.
10. For a process, preserve the order of the stages.
11. Keep the answer concise.
12. Do not mention the evidence, chunks, retrieval, or these rules.
13. Do not use your general knowledge.

Student question:
{question}

Evidence:
{context}

Answer:
""".strip()

    def _synthesize(
        self,
        question: str,
        chunks: List[Dict[str, Any]],
    ) -> str:
        """Use Ollama for explicitly enabled multi-evidence synthesis."""
        prompt = self._build_synthesis_prompt(
            question,
            chunks,
        )

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            options={
                "temperature": 0,
            },
        )

        message = response.get(
            "message",
            {},
        )

        answer = str(
            message.get(
                "content",
                "",
            )
        ).strip()

        if not answer:
            return INSUFFICIENT_CONTEXT_MESSAGE

        return answer

    def answer(
        self,
        question: str,
        chunks: List[Dict[str, Any]],
    ) -> str:
        """
        Generate an answer from retrieved evidence.

        The default behavior is evidence-first and extractive:
        - one strong explanatory chunk is returned directly;
        - multiple explanatory chunks are combined directly;
        - low-value question/exercise chunks are removed when possible.

        Ollama synthesis is optional and disabled by default because
        the retrieved lesson evidence must remain the source of truth.
        """
        if not question.strip():
            return INSUFFICIENT_CONTEXT_MESSAGE

        if not chunks:
            return INSUFFICIENT_CONTEXT_MESSAGE

        if self._is_single_direct_answer(chunks):
            return self._get_text(chunks[0])

        usable_chunks = self._filter_low_value_chunks(chunks)

        if usable_chunks:
            if not self.use_llm:
                return self._build_extractive_answer(
                    usable_chunks
                )

            return self._synthesize(
                question,
                usable_chunks,
            )

        return INSUFFICIENT_CONTEXT_MESSAGE