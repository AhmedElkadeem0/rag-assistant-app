# ⚡ RAG-Powered Technical Document Assistant

An end-to-end **Retrieval-Augmented Generation (RAG)** web application built as an **ITI Level 2 Summer Training Graduation Project — Core Track**.

The system allows users to ask questions about technical documentation and receive **grounded, citation-backed answers** generated from relevant document content.

It combines:

- 📄 PDF document ingestion
- ✂️ Recursive text chunking
- 🧠 Sentence-Transformers embeddings
- 🔎 Semantic similarity search
- 🗃️ Persistent ChromaDB vector storage
- ⚡ FastAPI REST API
- 🤖 Local Ollama LLM inference
- 💬 Interactive Streamlit frontend
- 📚 Source-aware responses
- 🧪 Basic RAG evaluation

The entire pipeline runs **locally**, without requiring a cloud-based LLM API.

---

## ✨ Key Features

- **Document-based Question Answering**  
  Ask technical questions against a predefined documentation corpus.

- **Retrieval-Augmented Generation**  
  Relevant document chunks are retrieved before generating the final answer.

- **Local Vector Database**  
  ChromaDB stores embeddings persistently on disk.

- **Local LLM Inference**  
  Uses Ollama with Qwen 2.5, keeping generation local.

- **Citation-Backed Answers**  
  Responses include the documents used to construct the answer.

- **Out-of-Domain Handling**  
  The system can decline questions when relevant information cannot be retrieved.

- **REST API**  
  FastAPI exposes `/health` and `/query` endpoints.

- **Interactive UI**  
  Streamlit provides a simple chat-style interface with source indicators.

- **Modular Architecture**  
  Retrieval, generation, API contracts, configuration, and frontend logic are separated into dedicated modules.

---

# 🏗️ Architecture

The application follows a standard RAG pipeline:

```text
                    ┌──────────────────────┐
                    │   Raw PDF Documents  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   PDF Text Extraction│
                    │        (pypdf)       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Recursive Chunking   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Sentence-Transformers│
                    │ all-MiniLM-L6-v2     │
                    └──────────┬───────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │       ChromaDB Vector Store    │
              │          Persistent Storage     │
              └───────────────┬────────────────┘
                              │
                              │ Semantic Retrieval
                              ▼
                    ┌──────────────────────┐
                    │    FastAPI Backend   │
                    │       /query         │
                    └──────────┬───────────┘
                               │
                        Retrieved Context
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Prompt Builder    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Ollama + Qwen 2.5  │
                    │     Local LLM        │
                    └──────────┬───────────┘
                               │
                        Grounded Answer
                        + Source Metadata
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Streamlit Frontend │
                    │   Interactive Chat   │
                    └──────────────────────┘
```

### RAG Workflow

```text
User Question
      │
      ▼
Generate Query Embedding
      │
      ▼
Search ChromaDB
      │
      ▼
Retrieve Relevant Chunks
      │
      ▼
Build Context + Prompt
      │
      ▼
Generate Answer with Qwen 2.5
      │
      ▼
Return Answer + Sources
```

---

# 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| PDF Processing | pypdf |
| Data Processing | NumPy, Pandas |
| Embeddings | Sentence-Transformers |
| Embedding Model | `all-MiniLM-L6-v2` |
| Vector Database | ChromaDB |
| LLM Runtime | Ollama |
| LLM | Qwen 2.5 |
| Backend | FastAPI |
| Validation | Pydantic |
| Server | Uvicorn |
| Frontend | Streamlit |
| HTTP Client | Requests |
| Testing | Pytest |
| Development | Jupyter Notebook |

---

# 📂 Project Structure

```text
rag-assistant-app/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── query.py
│   │   │
│   │   ├── core/
│   │   │   └── config.py
│   │   │
│   │   ├── schemas/
│   │   │   └── query.py
│   │   │
│   │   ├── services/
│   │   │   ├── retrieval/
│   │   │   └── generation/
│   │   │
│   │   └── main.py
│   │
│   ├── data/
│   │   └── vector_store/
│   │
│   ├── tests/
│   │
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── api_client.py
│   ├── app.py
│   └── requirements.txt
│
├── notebooks/
│   └── rag_pipeline.ipynb
│
├── data/
│   └── raw_docs/
│
├── .gitignore
└── README.md
```

> **Note:** The generated ChromaDB vector store is intentionally excluded from Git because it can be recreated from the source documents using the RAG pipeline notebook.

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/AhmedElkadeem0/rag-assistant-app.git
cd rag-assistant-app
```

---

## 2. Create a Virtual Environment

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install Dependencies

Upgrade pip:

```bash
pip install --upgrade pip
```

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

Install frontend dependencies:

```bash
pip install -r frontend/requirements.txt
```

---

# 🤖 4. Install and Configure Ollama

The project uses **Ollama** to run the LLM locally.

Install Ollama for your operating system, then download the required model:

```bash
ollama pull qwen2.5:1.5b
```

You can also use:

```bash
ollama pull qwen2.5:3b
```

The `1.5b` model is lighter and requires fewer resources, while the `3b` model can provide stronger generation quality at the cost of additional system resources.

Verify that the model is available:

```bash
ollama list
```

---

# 📚 5. Build the Vector Store

The repository includes a Jupyter notebook containing the document-processing pipeline:

```text
notebooks/rag_pipeline.ipynb
```

Run the notebook **from top to bottom**.

The notebook performs the following steps:

```text
PDF Documents
     │
     ▼
Text Extraction
     │
     ▼
Text Cleaning
     │
     ▼
Recursive Chunking
     │
     ▼
Embedding Generation
     │
     ▼
ChromaDB Persistence
```

The resulting vector database is stored under:

```text
backend/data/vector_store/
```

Make sure your source PDFs are available under:

```text
data/raw_docs/
```

before running the notebook.

---

# 🏃 Running the Application

The application consists of two services:

```text
Streamlit Frontend
       │
       │ HTTP
       ▼
FastAPI Backend
       │
       ├── ChromaDB
       │
       └── Ollama
```

## Step 1 — Start the FastAPI Backend

From the project root:

```bash
cd backend
```

Then run:

### Linux / macOS

```bash
PYTHONPATH=. uvicorn app.main:app --reload
```

### Windows

```powershell
$env:PYTHONPATH="."
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive Swagger documentation:

```text
http://localhost:8000/docs
```

---

## Step 2 — Start the Streamlit Frontend

Open a second terminal and activate the virtual environment.

From the project root:

```bash
cd frontend
streamlit run app.py
```

The frontend will be available at:

```text
http://localhost:8501
```

---

# 🔌 API Reference

## `GET /health`

Checks whether the backend is running correctly.

Example:

```bash
curl http://localhost:8000/health
```

---

## `POST /query`

Accepts a technical question and returns a grounded answer with source information.

### Request

```json
{
  "question": "What is microservices architecture?"
}
```

### cURL Example

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"question":"What is microservices architecture?"}'
```

### Response

The API returns the generated answer together with the retrieved source information.

A simplified response structure is:

```json
{
  "answer": "Microservices architecture is an architectural style...",
  "sources": [
    {
      "document": "microservices_guide.pdf"
    }
  ]
}
```

> The exact response fields depend on the current Pydantic response schema implemented in the project.

---

# 🧪 Evaluation

The system was evaluated using a set of questions covering the technical documentation corpus, along with an out-of-domain question.

| Test Question | Expected Source | Result |
|---|---|---|
| What is microservices architecture? | `microservices_guide.pdf` | ✅ Correct |
| What pattern solves data consistency? | `microservices_guide.pdf` | ✅ Correct |
| What tool handles service discovery? | `microservices_guide.pdf` | ✅ Correct |
| How do lifespan events help FastAPI performance? | `fastapi_best_practices.pdf` | ✅ Correct |
| What Pydantic model validates requests? | `fastapi_best_practices.pdf` | ✅ Correct |
| Why add CORSMiddleware? | `fastapi_best_practices.pdf` | ✅ Correct |
| What does Cosine Similarity measure? | `vector_database_fundamentals.pdf` | ✅ Correct |
| What are the two types of chunking strategies? | `vector_database_fundamentals.pdf` | ✅ Correct |
| What step comes first in the RAG pipeline? | `vector_database_fundamentals.pdf` | ✅ Correct |
| Who won the 1998 World Cup? | None | ✅ Correctly declined |

### Evaluation Goals

The evaluation focuses on three main aspects:

1. **Retrieval relevance** — whether the appropriate document is retrieved.
2. **Answer grounding** — whether the generated response is supported by retrieved context.
3. **Out-of-domain behavior** — whether the system avoids fabricating an answer when relevant information is unavailable.

> This evaluation is a small functional test set rather than a statistically comprehensive benchmark.

---

# 🔐 Grounding & Out-of-Domain Behavior

A key objective of the system is to reduce hallucination by restricting generation to retrieved document context.

Conceptually:

```text
Question
   │
   ▼
Retriever
   │
   ├── Relevant Context Found
   │          │
   │          ▼
   │      LLM Generation
   │          │
   │          ▼
   │    Grounded Answer
   │
   └── No Relevant Context
              │
              ▼
       Decline / No Answer
```

For example, when asked:

> **Who won the 1998 World Cup?**

the system does not have relevant information in its technical documentation corpus and therefore declines to answer rather than using unrelated external knowledge.

---

# 🧩 Design Decisions

## Why RAG?

A standard LLM can generate answers from its pretrained knowledge, but it may not know the specific content of a private or custom documentation corpus.

RAG addresses this by separating the process into:

```text
Retrieval → Context → Generation
```

The model receives relevant document chunks as context before generating its response.

---

## Why Sentence-Transformers?

The project uses:

```text
all-MiniLM-L6-v2
```

to convert text into numerical vector representations.

These embeddings allow semantically similar questions and document chunks to be compared even when they do not use exactly the same words.

---

## Why ChromaDB?

ChromaDB provides a lightweight vector database suitable for a local RAG application.

The project uses persistent storage so embeddings do not need to be regenerated every time the backend starts.

---

## Why Ollama?

Ollama allows the application to run an LLM locally instead of depending on an external inference API.

This provides:

- Local inference
- No per-request API costs
- Better control over data
- Easy model switching

---

## Why FastAPI?

FastAPI separates the RAG logic from the frontend and provides a clean REST interface.

This also makes it possible to replace the Streamlit frontend with another client in the future.

---

# 🖥️ Frontend

The Streamlit interface provides:

- 💬 Chat-style interaction
- 🔎 Technical question input
- 🤖 Generated answers
- 📚 Retrieved source information
- 🏷️ Status / source badges
- ⚡ Simple interactive experience

The frontend communicates with the backend exclusively through the FastAPI API.

---

# 🧪 Testing

The backend includes a Pytest test suite under:

```text
backend/tests/
```

Run the tests with:

```bash
pytest
```

For more verbose output:

```bash
pytest -v
```

---

# 🐳 Docker

The backend includes a Dockerfile:

```text
backend/Dockerfile
```

The Docker configuration can be used to containerize the FastAPI service.

> Ollama and the local vector store still need to be handled separately depending on the deployment environment.

---

# 📌 Current Limitations

This project is designed as an educational graduation project and currently has several limitations:

- The document corpus is relatively small.
- Evaluation is based on a limited manually created test set.
- Retrieval quality depends on the selected embedding model and chunking strategy.
- Local LLM performance depends heavily on available hardware.
- The current application does not provide authentication or user management.
- The vector database is generated locally rather than distributed.
- The system is currently designed for a predefined technical documentation corpus.

---

# 🔮 Future Improvements

Potential improvements include:

- [ ] Hybrid search combining semantic and keyword retrieval
- [ ] Reranking retrieved chunks
- [ ] Improved chunking strategies
- [ ] Metadata filtering
- [ ] Automatic evaluation using RAG metrics
- [ ] Larger and more diverse evaluation datasets
- [ ] Streaming LLM responses
- [ ] Conversation memory
- [ ] Document upload through the UI
- [ ] Authentication and user management
- [ ] Production-ready deployment
- [ ] Monitoring and logging
- [ ] Support for additional embedding and LLM models

---

# 🎓 Project Context

**Program:** ITI — Information Technology Institute  
**Training:** Level 2 Summer Training  
**Track:** Core Track  
**Project Type:** Graduation Project  
**Domain:** Retrieval-Augmented Generation / Generative AI

---

# 👨‍💻 Author

**Ahmed Elkadeem**

Computer Science Student | Cybersecurity Enthusiast

GitHub:  
https://github.com/AhmedElkadeem0

---

# 📄 License

This project was developed for educational and training purposes as part of the ITI Summer Training Graduation Project.