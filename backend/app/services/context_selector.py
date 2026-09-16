
"""Context selection utilities for the RAG pipeline."""

from typing import Any, Dict, List


MAX_CONTEXT_CHUNKS = 4
DEFAULT_RELEVANCE_MARGIN = 0.05


class ContextSelector:
    """Select a focused set of evidence chunks."""

    def __init__(
        self,
        max_chunks: int = MAX_CONTEXT_CHUNKS,
        relevance_margin: float = DEFAULT_RELEVANCE_MARGIN,
    ) -> None:
        """Initialize the context selector."""
        if max_chunks < 1:
            raise ValueError(
                "max_chunks must be greater than zero."
            )

        if relevance_margin < 0:
            raise ValueError(
                "relevance_margin cannot be negative."
            )

        self.max_chunks = max_chunks
        self.relevance_margin = relevance_margin

    @staticmethod
    def _content_type(
        chunk: Dict[str, Any],
    ) -> str:
        """Return a chunk content type safely."""
        metadata = chunk.get(
            "metadata",
            {},
        )

        if not isinstance(metadata, dict):
            return ""

        return str(
            metadata.get(
                "content_type",
                "",
            )
        )

    @staticmethod
    def _distance(
        chunk: Dict[str, Any],
    ) -> float:
        """Return a chunk distance safely."""
        try:
            return float(
                chunk.get(
                    "distance",
                    float("inf"),
                )
            )
        except (TypeError, ValueError):
            return float("inf")

    @staticmethod
    def _process_sort_key(
        chunk: Dict[str, Any],
    ) -> int:
        """Return the explicit process step number."""
        metadata = chunk.get(
            "metadata",
            {},
        )

        if not isinstance(metadata, dict):
            return 10**9

        try:
            return int(
                metadata.get(
                    "step_number",
                    10**9,
                )
            )
        except (TypeError, ValueError):
            return 10**9

    @staticmethod
    def _is_process_question(
        question: str,
    ) -> bool:
        """Detect whether the question asks about a process."""
        normalized = question.strip().lower()

        process_terms = (
            "how does",
            "how do",
            "how is",
            "how are",
            "steps",
            "stages",
            "process",
            "كيف يعمل",
            "كيف تعمل",
            "كيف يتم",
            "خطوات",
            "مراحل",
            "عملية",
        )

        return any(
            term in normalized
            for term in process_terms
        )

    @classmethod
    def _remove_low_value_chunks(
        cls,
        chunks: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """Remove question and exercise chunks when better evidence exists."""
        if not chunks:
            return []

        explanatory_types = {
            "concept",
            "process",
            "summary",
            "example",
        }

        has_explanatory = any(
            cls._content_type(chunk)
            in explanatory_types
            for chunk in chunks
        )

        if not has_explanatory:
            return chunks

        filtered = [
            chunk
            for chunk in chunks
            if cls._content_type(chunk)
            not in {
                "question",
                "exercise",
            }
        ]

        return filtered or chunks

    @classmethod
    def _select_by_relevance(
        cls,
        chunks: List[Dict[str, Any]],
        max_chunks: int,
        relevance_margin: float,
    ) -> List[Dict[str, Any]]:
        """
        Keep the strongest cluster of results.

        A chunk is retained when its distance is close enough to the
        best retrieved distance. This prevents weakly related chunks
        from flooding the answer context.
        """
        if not chunks:
            return []

        ranked = sorted(
            chunks,
            key=cls._distance,
        )

        best_distance = cls._distance(
            ranked[0]
        )

        selected = [
            chunk
            for chunk in ranked
            if (
                cls._distance(chunk)
                <= best_distance + relevance_margin
            )
        ]

        return selected[:max_chunks]

    @classmethod
    def _select_process_chunks(
        cls,
        chunks: List[Dict[str, Any]],
        max_chunks: int,
        relevance_margin: float,
    ) -> List[Dict[str, Any]]:
        """
        Select relevant process chunks and preserve their order.

        Process structure is used only after relevance has identified
        a strong group of process evidence. This prevents a specific
        process-stage question from automatically receiving every
        process stage.
        """
        process_chunks = [
            chunk
            for chunk in chunks
            if cls._content_type(chunk) == "process"
        ]

        if not process_chunks:
            return []

        ranked = sorted(
            process_chunks,
            key=cls._distance,
        )

        best_distance = cls._distance(
            ranked[0]
        )

        selected = [
            chunk
            for chunk in ranked
            if (
                cls._distance(chunk)
                <= best_distance + relevance_margin
            )
        ]

        selected.sort(
            key=cls._process_sort_key,
        )

        return selected[:max_chunks]

    def select(
        self,
        question: str,
        chunks: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Select focused evidence for answer generation.

        Retrieval ranking remains the primary relevance signal.
        Structural metadata is used to:
        - preserve process order,
        - remove low-value exercise/question chunks,
        - prevent unrelated retrieved chunks from flooding context.
        """
        if not question.strip():
            raise ValueError(
                "Question cannot be empty."
            )

        if not chunks:
            return []

        ranked_chunks = sorted(
            chunks,
            key=self._distance,
        )

        ranked_chunks = self._remove_low_value_chunks(
            ranked_chunks
        )

        if not ranked_chunks:
            return []

        if self._is_process_question(question):
            process_chunks = self._select_process_chunks(
                ranked_chunks,
                self.max_chunks,
                self.relevance_margin,
            )

            if process_chunks:
                return process_chunks

        return self._select_by_relevance(
            ranked_chunks,
            self.max_chunks,
            self.relevance_margin,
        )
