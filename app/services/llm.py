from functools import lru_cache

from groq import Groq

# Project Imports
from app.core.config import settings
from app.core.constants import TEMPERATURE


# Groq Client ek patak create garera reuse garne
@lru_cache(maxsize=1)
def get_groq_client() -> Groq:
    return Groq(api_key=settings.groq_api_key)


def generate_answer(
    question: str,
    context: str,
) -> str:

    client = get_groq_client()

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    "Answer the user's question using only the "
                    "provided context. "
                    "If the context does not contain the answer, "
                    "clearly say that the information is not "
                    "available in the provided documents. "
                    "Do not make up information."
                ),
            },
            {
                "role": "user",
                "content": (f"Context:\n{context}\n\n" f"Question:\n{question}"),
            },
        ],
        temperature=TEMPERATURE,
    )

    answer = response.choices[0].message.content

    if not answer:
        raise ValueError("Groq returned an empty response.")

    return answer.strip()
