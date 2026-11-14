from app.services.chunking import create_chunks

sample_text = """
Python is a programming language.
Python supports object-oriented programming.
Python is widely used in backend development.
Apple is my favourite fruit.
My friend worked at Apple company.
The earth revolves around the sun.
The solar system contains multiple planets.
"""


recursive_chunks = create_chunks(
    texts=sample_text,
    strategy="recursive",
)

semantic_chunks = create_chunks(
    texts=sample_text,
    strategy="semantic",
)

print("RECURSIVE CHUNKS:")

for chunk in recursive_chunks:
    print(chunk)


print("\nSEMANTIC CHUNKS:")
for chunk in semantic_chunks:
    print(chunk)
