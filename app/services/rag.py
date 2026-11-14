# Project Imports
from app.services.retrieval import retrieve_chunks
from app.services.llm import generate_answer


def generate_rag_answer(question: str) -> str:

    # Relevant chunks Qdrant bata retrieve garne
    chunks = retrieve_chunks(
        query=question,
        limit=5,
    )

    if not chunks:
        return "No relevant information found in the documents."

    # Retrieved chunks lai euta context ma combine garne
    context = "\n\n".join(chunks)

    # Context ra question Groq LLM lai pathaune
    answer = generate_answer(
        question=question,
        context=context,
    )

    return answer
