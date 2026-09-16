
"""Tests for the FastAPI application."""

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint() -> None:
    """The health endpoint should return a healthy status."""
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }


def test_query_endpoint_happy_path() -> None:
    """A valid question should return an answer and sources."""
    with TestClient(app) as client:
        response = client.post(
            "/query",
            json={
                "question": "What is the possession factor?",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "sources" in data

    assert isinstance(data["answer"], str)
    assert data["answer"].strip()

    assert isinstance(data["sources"], list)
    assert data["sources"]


def test_query_endpoint_rejects_empty_question() -> None:
    """An empty question should return HTTP 422."""
    with TestClient(app) as client:
        response = client.post(
            "/query",
            json={
                "question": "",
            },
        )

    assert response.status_code == 422


def test_query_endpoint_rejects_whitespace_question() -> None:
    """A whitespace-only question should return HTTP 422."""
    with TestClient(app) as client:
        response = client.post(
            "/query",
            json={
                "question": "   ",
            },
        )

    assert response.status_code == 422


def test_query_endpoint_rejects_missing_question() -> None:
    """A request without a question should return HTTP 422."""
    with TestClient(app) as client:
        response = client.post(
            "/query",
            json={},
        )

    assert response.status_code == 422
