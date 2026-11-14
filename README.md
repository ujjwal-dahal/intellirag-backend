# 🧠 IntelliRAG — Backend

IntelliRAG is a **Retrieval-Augmented Generation (RAG)** backend built with **FastAPI**. It ingests documents, splits them into meaningful chunks, stores their embeddings in a vector database, and retrieves the most relevant context to answer user questions accurately.

---

## ✨ Features

- 📄 Document ingestion with **two chunking strategies**
- 🔍 Fast vector search using **HNSW indexing**
- 📐 **Cosine similarity** for semantic matching
- ⚡ Redis-based caching with **Upstash**
- 🗄️ Persistent relational storage with **Neon (PostgreSQL)** + **SQLAlchemy**
- 🚀 high-performance REST API with **FastAPI**

---

## 🛠️ Tech Stack

| Layer           | Technology                          |
| --------------- | ----------------------------------- |
| API Framework   | FastAPI                             |
| Relational DB   | Neon Database (Serverless Postgres) |
| ORM             | SQLAlchemy                          |
| Vector DB       | Qdrant Cloud                        |
| Cache           | Upstash Redis                       |
| Package Manager | uv                                  |

---

## 🧩 RAG Pipeline Design

### 1. Chunking Strategies

IntelliRAG supports two ways of splitting documents:

1. **Recursive Character Splitter**
   Splits text by a hierarchy of separators (paragraphs → sentences → words → characters) with a configurable chunk size and overlap. Fast and predictable.

2. **Semantic Chunking**
   Splits text based on _meaning_. Sentences with similar semantics are grouped together, and a new chunk starts where the topic shifts. Produces more coherent chunks and better retrieval quality.

### 2. Embeddings

- Embedding dimension: **384**
- Every chunk and every user query is converted into a 384-dimensional vector.

### 3. Vector Indexing & Search

- **Index algorithm:** HNSW (Hierarchical Navigable Small World)
  A graph-based approximate nearest neighbour algorithm that makes searching very fast, even with a large number of vectors.
- **Distance metric:** Cosine Similarity
  Measures the angle between vectors, so it focuses on semantic meaning rather than vector magnitude.

### 4. Flow

```
Document → Chunking → Embedding (384-d) → Qdrant (HNSW, cosine)
                                                  │
User Query → Embedding (384-d) → Similarity Search ┘ → Top-K chunks → Answer
```

---

## 📁 Project Structure

```
intellirag-backend/
├── app/
│   ├── api/          # API routes / endpoints
│   ├── core/         # Config, settings, security, clients
│   ├── database/     # SQLAlchemy models, session, DB setup
│   ├── schemas/      # Pydantic request/response schemas
│   ├── utils/        # Helpers (chunking, embeddings, etc.)
│   ├── __init__.py
│   └── main.py       # FastAPI entry point
├── src/
├── .env.example      # Example environment variables
├── .gitignore
├── .python-version
├── pyproject.toml    # Dependencies (uv)
├── uv.lock
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python (version in `.python-version`)
- [uv](https://docs.astral.sh/uv/) installed
- Accounts for: [Neon](https://neon.tech), [Qdrant Cloud](https://cloud.qdrant.io), [Upstash](https://upstash.com)

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd intellirag-backend
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Then fill in your values in `.env`:

```env
# Neon (PostgreSQL)
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require

# Qdrant Cloud
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key

# Upstash Redis
UPSTASH_REDIS_REST_URL=https://your-upstash-url
UPSTASH_REDIS_REST_TOKEN=your_upstash_token
```

> ⚠️ Variable names above are examples — keep them the same as in your `.env.example`.

### 4. Run the server

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

- API: `http://127.0.0.1:8000`
- Swagger Docs: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## 🔐 Environment & Security

- Never commit your `.env` file (it is already in `.gitignore`).
- Only commit `.env.example` with placeholder values.

---

## 👨‍💻 Author

**Ujjwal Dahal**
GitHub: [@ujjwal-dahal](https://github.com/ujjwal-dahal)
