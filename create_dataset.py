import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

docs_dir = "data/raw_docs"
os.makedirs(docs_dir, exist_ok=True)

documents = {
    "microservices_guide.pdf": [
        ("Microservices Architecture Overview", "Heading1"),
        ("Microservices architecture decomposes applications into small, independent services. Each service communicates via lightweight REST APIs or gRPC protocols.", "Normal"),
        ("Key Benefits", "Heading2"),
        ("1. Fault Isolation: A crash in one module does not bring down the whole application.", "Normal"),
        ("2. Scalability: Individual services can scale horizontally based on demand.", "Normal"),
        ("3. Deployment Speed: Independent CI/CD pipelines allow rapid delivery.", "Normal"),
        ("Common Challenges", "Heading2"),
        ("Data Consistency: Distributed transactions require event-driven architecture such as the Saga pattern.", "Normal"),
        ("Service Discovery: Dynamic IP management requires tools like Consul or Kubernetes DNS.", "Normal")
    ],
    "fastapi_best_practices.pdf": [
        ("FastAPI High-Performance Framework Guide", "Heading1"),
        ("FastAPI relies on Python type hints and Pydantic for fast execution and high developer velocity.", "Normal"),
        ("Application Lifespan Events", "Heading2"),
        ("Using lifespan async context managers allows startup resources—such as database pools or vector stores—to be pre-loaded into memory once before handling requests.", "Normal"),
        ("Request Validation and Security", "Heading2"),
        ("Enforce input schemas using Pydantic BaseModel to ensure strict API data contracts.", "Normal"),
        ("Add CORSMiddleware to allow requests securely from frontend application origins.", "Normal")
    ],
    "vector_database_fundamentals.pdf": [
        ("Vector Search and Embeddings Deep Dive", "Heading1"),
        ("Vector databases index high-dimensional vector representations of unstructured text data.", "Normal"),
        ("Chunking Strategies", "Heading2"),
        ("Fixed-size Chunking: Splits text every N characters with fixed overlap.", "Normal"),
        ("Recursive Character Chunking: Respects natural structural boundaries such as paragraphs and headers.", "Normal"),
        ("Similarity Metrics", "Heading2"),
        ("Cosine Similarity: Measures the angular distance between vectors, ideal for text embeddings.", "Normal"),
        ("Euclidean Distance: Measures straight-line spatial distance between points.", "Normal"),
        ("Query Pipeline Sequence", "Heading2"),
        ("1. Embed the user query string using the sentence embedding model.", "Normal"),
        ("2. Query the vector collection for Top-K nearest neighbors.", "Normal"),
        ("3. Pass retrieved document chunks alongside the original user prompt to the local LLM.", "Normal")
    ]
}

styles = getSampleStyleSheet()

for filename, content in documents.items():
    file_path = os.path.join(docs_dir, filename)
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    story = []
    
    for text, style_name in content:
        story.append(Paragraph(text, styles[style_name]))
        story.append(Spacer(1, 8))
        
    doc.build(story)
    print(f"Created: {file_path}")

print("\nDataset creation complete.")