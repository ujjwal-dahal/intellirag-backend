from langchain_text_splitters import RecursiveCharacterTextSplitter

import re
import numpy as np

# Project Imports
from app.services.embedding import get_embedding_model


def recursive_chunking(texts: str, chunk_size: int = 800, chunk_overlap: int = 120):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = splitter.split_text(texts)

    return chunks


def semantic_chunking(
    texts: str,
    similarity_threshold: float = 0.65,
    max_chunk_size: int = 1000,
):

    # Texts lai Sentences ma Divide using Regex
    sentences = re.split(
        r"(?<=[.!?])\s+",
        texts.strip(),
    )

    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

    if not sentences:
        return []

    # Dherai Long sentence lai sano parts ma divide garne
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_chunk_size,
        chunk_overlap=0,
        separators=["\n\n", "\n", " ", ""],
    )

    processed_sentences = []

    for sentence in sentences:

        if len(sentence) > max_chunk_size:
            processed_sentences.extend(splitter.split_text(sentence))
        else:
            processed_sentences.append(sentence)

    if len(processed_sentences) == 1:
        return processed_sentences

    # Sentence embeddings generate garne
    model = get_embedding_model()

    embeddings = model.encode(
        processed_sentences,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    )

    chunks = []

    current_chunk = processed_sentences[0]

    # Semantic Chunking Main Logic
    for index in range(1, len(processed_sentences)):

        previous_sentence_embedding = embeddings[index - 1]
        next_sentence_embedding = embeddings[index]

        # Previous ra Next Sentence ko Similarity calculate garne
        similarity = float(
            np.dot(
                previous_sentence_embedding,
                next_sentence_embedding,
            )
        )

        next_sentence = processed_sentences[index]

        combined_length = len(current_chunk) + 1 + len(next_sentence)

        # Meaning similar cha ra size limit vitra cha bhane merge garne
        if similarity >= similarity_threshold and combined_length <= max_chunk_size:
            current_chunk += " " + next_sentence

        else:
            chunks.append(current_chunk)
            current_chunk = next_sentence

    # Adding Last Chunk
    chunks.append(current_chunk)

    return chunks


def create_chunks(
    texts: str,
    strategy: str,
) -> list[str]:

    if strategy == "recursive":
        return recursive_chunking(texts)

    if strategy == "semantic":
        return semantic_chunking(texts)

    raise ValueError("Unsupported chunking strategy.")
