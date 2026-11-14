# Maximum Upload Size = 15 MB
MAX_UPLOAD_SIZE = 15 * 1024 * 1024

# Qdrant
COLLECTION_NAME = "rag-documents"

# HNSW Parameters
M = 16
EF_CONSTRUCT = 100
HNSW_EF = 128

# all-MiniLM-L6-v2 embedding dimension
VECTOR_SIZE = 384

# Recursive Chunking
CHUNK_SIZE = 800
CHUNK_OVERLAP = 120

# Semantic Chunking
SIMILARITY_THRESHOLD = 0.65
MAX_CHUNK_SIZE = 1000

# LLM Parameters
TEMPERATURE = 0.2


# Redis
CHAT_HISTORY_LIMIT = 10
CHAT_MEMORY_TTL = 60 * 60 * 24 * 7
