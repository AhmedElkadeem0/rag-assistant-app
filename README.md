⚡ RAG-Powered Technical Document AssistantAn end-to-end Retrieval-Augmented Generation (RAG) web application built for the ITI Level 2 Summer Training Graduation Project (Core Track). This system ingests technical documentation, stores embedded vectors locally, and serves grounded, citation-backed answers via a FastAPI backend and an interactive Streamlit UI.🏗️ Architecture & Data Flow[ Raw PDF Documents ] 
        │
        ▼ (pypdf Extraction & Recursive Chunking)
[ Sentence-Transformers (all-MiniLM-L6-v2) ]
        │
        ▼ (Vector Embeddings)
[ ChromaDB Persistent Vector Store ] ◄─── (Loaded via FastAPI Lifespan)
        │
        ▼
[ FastAPI Backend (/query) ] ──(Context + Prompt)──► [ Local Ollama LLM (Qwen 2.5) ]
        │                                                     │
        └────────────────────◄── (Grounded Answer + Sources) ───┘
        │
        ▼
[ Streamlit Frontend UI (Interactive Chat & Badges) ]

🛠️ Tech StackLanguage: Python 3.10+Data Processing: pypdf, pandas, numpyEmbeddings & Vector Store: sentence-transformers (all-MiniLM-L6-v2), ChromaDB (Persistent)Local LLM Engine: Ollama (qwen2.5:1.5b or qwen2.5:3b)Backend API: FastAPI, Pydantic, Uvicorn, pytestFrontend UI: Streamlit, Requests📂 Project Structurerag-assistant-app/
├── backend/
│   ├── app/
│   │   ├── api/routes/query.py   # /health and /query endpoints
│   │   ├── core/config.py        # Centralized settings (.env parser)
│   │   ├── schemas/query.py      # Pydantic request/response validation contracts
│   │   ├── services/             # Retrieval & Ollama LLM generation logic
│   │   └── main.py               # FastAPI application lifespan & CORS setup
│   ├── data/vector_store/        # Persisted ChromaDB vector database (Ignored in Git)
│   ├── tests/                    # Pytest unit testing suite
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── api_client.py             # Modular wrapper for FastAPI REST calls
│   ├── app.py                    # Streamlit interactive UI
│   └── requirements.txt
├── notebooks/
│   └── rag_pipeline.ipynb        # End-to-end data processing, chunking & evaluation notebook
├── data/raw_docs/                # Source PDF technical documentation corpus
├── .gitignore
└── README.md

🚀 Local Setup & Installation Instructions1. Clone the Repositorygit clone https://github.com/AhmedElkadeem0/rag-assistant-app.git
cd rag-assistant-app

2. Set Up Virtual Environment & Install Dependenciespython -m venv .venv
# Activate environment:
# On Windows: .venv\Scripts\activate
# On Linux/macOS: source .venv/bin/activate (or source .venv/bin/activate.fish for Fish shell)

pip install --upgrade pip
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

3. Ensure Local Ollama Model is RunningMake sure Ollama is installed and your model is downloaded locally:ollama pull qwen2.5:1.5b

4. Build or Load the Vector StoreOpen and run notebooks/rag_pipeline.ipynb top-to-bottom inside Jupyter to parse the sample PDFs, create embeddings, and persist the vector database directly into backend/data/vector_store/.🏃‍♂️ Running the ApplicationStep 1: Start the FastAPI BackendOpen terminal 1, activate your virtual environment, and run the backend server:cd backend
env PYTHONPATH=. uvicorn app.main:app --reload

Interactive Swagger API documentation will be live at: http://localhost:8000/docsStep 2: Start the Streamlit FrontendOpen terminal 2, activate your virtual environment, and run the frontend application:cd frontend
streamlit run app.py

The Streamlit user interface will be live at: http://localhost:8501🧪 API Reference & cURL ExampleGET /health: Returns system operational status.POST /query: Accepts a technical question payload and returns a grounded response with source document citations.curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is microservices architecture?"}'

📊 Evaluation Results Matrix| Test Question | Retrieved Sources | Grounded / Correct? || What is microservices architecture? | microservices_guide.pdf | Yes || What pattern solves data consistency? | microservices_guide.pdf | Yes || What tool handles service discovery? | microservices_guide.pdf | Yes || How do lifespan events help FastAPI performance? | fastapi_best_practices.pdf | Yes || What Pydantic model validates requests? | fastapi_best_practices.pdf | Yes || Why add CORSMiddleware? | fastapi_best_practices.pdf | Yes || What does Cosine Similarity measure? | vector_database_fundamentals.pdf | Yes || What are the two types of chunking strategies? | vector_database_fundamentals.pdf | Yes || What step comes first in the RAG pipeline? | vector_database_fundamentals.pdf | Yes || Who won the 1998 World Cup? (Out-of-domain) | None | N/A (Declined correctly) |