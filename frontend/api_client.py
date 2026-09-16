import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def check_backend_health() -> bool:
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def query_rag_api(question: str) -> dict:
    url = f"{API_BASE_URL}/query"
    payload = {"question": question}
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return {"error": f"API Error: {response.status_code} - {response.text}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Could not connect to the backend server. Make sure FastAPI is running on port 8000."}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. The LLM engine took too long to respond."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}