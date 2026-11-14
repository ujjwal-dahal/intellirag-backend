# 🧠 IntelliRAG — Backend

IntelliRAG is a **Retrieval-Augmented Generation (RAG)** backend built with **FastAPI**. It allows users to upload PDF and TXT documents, processes them using different chunking strategies, generates embeddings, and stores them in Qdrant for semantic search.

It also supports conversational RAG with Redis-based chat memory and an AI-powered interview booking system.

---

## ✨ Features

- 📄 **Document Ingestion:** Upload PDF and TXT documents.
- 🧩 **Multiple Chunking Strategies:** Recursive character splitting and semantic chunking.
- 🧠 **Text Embeddings:** Convert document chunks and user queries into vector embeddings.
- 🔍 **Semantic Search:** Retrieve relevant document chunks using Qdrant.
- ⚡ **Vector Indexing:** HNSW indexing with cosine similarity.
- 💬 **Conversational RAG:** Answer questions using retrieved document context.
- 🧵 **Chat Memory:** Maintain conversation history using Upstash Redis.
- 📅 **Interview Booking:** Collect and validate interview details through an AI-powered conversation.
- 🗄️ **Persistent Storage:** Store document metadata and interview bookings in Neon PostgreSQL.
- 🚀 **REST API:** Built with FastAPI and documented using Swagger UI.

---

## 🛠️ Tech Stack

| Layer                | Technology            |
| -------------------- | --------------------- |
| Programming Language | Python                |
| API Framework        | FastAPI               |
| LLM Provider         | Groq                  |
| Embedding Model      | Sentence Transformers |
| Relational Database  | Neon PostgreSQL       |
| ORM                  | SQLAlchemy            |
| Vector Database      | Qdrant Cloud          |
| Vector Index         | HNSW                  |
| Similarity Metric    | Cosine Similarity     |
| Cache & Chat Memory  | Upstash Redis         |
| PDF Processing       | PyMuPDF               |
| Package Manager      | uv                    |
| Data Validation      | Pydantic              |

---

## 🧩 RAG Pipeline Design

### 1. Document Ingestion

IntelliRAG supports PDF and TXT document uploads.

The ingestion process follows these steps:

1. Validate the uploaded file.
2. Extract text from the document.
3. Split extracted text into chunks.
4. Generate embeddings for each chunk.
5. Store document metadata in PostgreSQL.
6. Store chunk embeddings and metadata in Qdrant.

### 2. Chunking Strategies

IntelliRAG supports two chunking strategies:

**1. Recursive Character Splitting**

- Splits text using a hierarchy of separators.
- Tries to preserve paragraphs and sentences.
- Uses configurable chunk size and overlap.
- Fast and predictable.

**2. Semantic Chunking**

- Splits text based on semantic meaning.
- Groups sentences with similar meanings.
- Starts a new chunk when the topic changes.
- Helps preserve meaningful context.

### 3. Embeddings

- Embedding dimension: **384**
- Each document chunk is converted into a 384-dimensional vector.
- User queries are also converted into vectors before retrieval.
- Sentence Transformers is used for embedding generation.

### 4. Vector Indexing & Search

**Index Algorithm: HNSW**

Hierarchical Navigable Small World (HNSW) is a graph-based approximate nearest neighbor algorithm used for efficient vector search.

**Distance Metric: Cosine Similarity**

Cosine similarity measures the angle between two vectors to determine how semantically similar they are.

### 5. RAG Flow

```text
             DOCUMENT INGESTION

PDF / TXT Document
        |
        v
   Text Extraction
        |
        v
      Chunking
        |
        v
    Embeddings
        |
        v
      Qdrant
  (HNSW + Cosine)
        |
        |
        v
             CONVERSATIONAL RAG

User Query
     |
     v
Query Embedding
     |
     v
Qdrant Similarity Search
     |
     v
Retrieve Top-K Chunks
     |
     v
Build Context + Chat History
     |
     v
      Groq LLM
     |
     v
   Final Answer
```

---

## 💬 Conversational RAG & Chat Memory

- Maintains conversation history using Upstash Redis.
- Uses a unique conversation ID to identify each conversation.
- Retrieves relevant document chunks for user queries.
- Uses previous conversation messages as context.
- Preserves recent chat messages for multi-turn conversations.
- Automatically expires Redis conversation data after the configured TTL.

---

## 📅 AI-Powered Interview Booking

IntelliRAG also supports interview booking through the same conversational chat endpoint.

**Booking Details:**

- Candidate Name
- Email Address
- Interview Date
- Interview Time

**Booking Flow:**

1. Detect whether the user wants to book an interview.
2. Extract booking details using Groq LLM.
3. Store collected details temporarily in Redis.
4. Ask for missing information.
5. Validate the collected information using Pydantic.
6. Ask the user to confirm the booking.
7. Save the confirmed booking in PostgreSQL.

---

## 📁 Project Structure

```text
intellirag-backend/
│
├── app/
│   ├── api/
│   │   ├── chat_routes.py
│   │   └── document_routes.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── constants.py
│   │
│   ├── database/
│   │   ├── base.py
│   │   ├── connection.py
│   │   ├── models.py
│   │   ├── init_db.py
│   │   └── qdrant.py
│   │
│   ├── schemas/
│   │   ├── booking.py
│   │   ├── chat.py
│   │   └── document.py
│   │
│   ├── services/
│   │   ├── booking.py
│   │   ├── booking_llm.py
│   │   ├── chat_memory.py
│   │   ├── chunking.py
│   │   ├── embedding.py
│   │   ├── ingestion.py
│   │   ├── intent.py
│   │   ├── llm.py
│   │   ├── rag.py
│   │   └── vector_store.py
│   │
│   ├── utils/
│   │   └── file_extractor.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── main.py
│
├── .env.example
├── .gitignore
├── .python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python version specified in `.python-version`
- [uv](https://docs.astral.sh/uv/) package manager
- [Groq](https://console.groq.com/) API key
- [Neon](https://neon.tech/) PostgreSQL database
- [Qdrant Cloud](https://cloud.qdrant.io/) account
- [Upstash](https://upstash.com/) Redis database

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd intellirag-backend
```

### 2. Install Dependencies

```bash
uv sync
```

### 3. Configure Environment Variables

Create your `.env` file:

```bash
cp .env.example .env
```

Configure the required environment variables:

```env
# Groq
GROQ_API_KEY=your_groq_api_key

# Neon PostgreSQL
DATABASE_URL=postgresql+psycopg://user:password@host/dbname?sslmode=require

# Qdrant Cloud
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_qdrant_api_key

# Upstash Redis
UPSTASH_REDIS_REST_URL=https://your-upstash-url
UPSTASH_REDIS_REST_TOKEN=your_upstash_token
```

> Note: Variable names should match the configuration defined in `.env.example` and the application settings.

### 4. Initialize Database Tables

Before starting the application, create the required PostgreSQL tables:

```bash
uv run python -m app.database.init_db
```

This creates the following tables:

- `documents_metadata`
- `interview_bookings`

### 5. Run the Application

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at:

| Service      | URL                          |
| ------------ | ---------------------------- |
| Home         | http://127.0.0.1:8000        |
| Swagger UI   | http://127.0.0.1:8000/docs   |
| ReDoc        | http://127.0.0.1:8000/redoc  |
| Health Check | http://127.0.0.1:8000/health |

---

## 🔐 Environment & Security

- Never commit your `.env` file.
- Keep API keys and database credentials private.
- Only commit `.env.example` with placeholder values.
- Validate uploaded files before processing.
- Use environment variables for sensitive configuration.

---

## 👨‍💻 Author

**Ujjwal Dahal**

GitHub: [@ujjwal-dahal](https://github.com/ujjwal-dahal)
