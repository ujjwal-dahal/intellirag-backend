import uuid

# Project Imports
from app.services.retrieval import retrieve_chunks
from app.services.llm import generate_answer
from app.services.chat_memory import get_chat_history, save_chat_message


def generate_rag_answer(question: str, conversation_id: str) -> str:

    # New Conversation Id create gareko If chaina bhane
    if not conversation_id:
        conversation_id = str(uuid.uuid4())

    # Retrieve Previous Chat History from Redis
    chat_history = get_chat_history(conversation_id=conversation_id)

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
        question=question, context=context, chat_history=chat_history
    )

    # Redis ma Save
    save_chat_message(conversation_id=conversation_id, role="user", content=question)

    save_chat_message(conversation_id=conversation_id, role="ai", content=answer)

    return answer, conversation_id
