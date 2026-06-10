import os

DOCS_DIR = "documents"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50


def load_documents():
    documents = []
    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(DOCS_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read().strip()
            if text:
                documents.append({
                    "source": filename,
                    "text": text
                })
    print(f"Loaded {len(documents)} document(s)")
    return documents


def chunk_document(doc):
    text = doc["text"]
    source = doc["source"]
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunks.append({
                "chunk_id": f"{source}_chunk_{chunk_index}",
                "source": source,
                "text": chunk_text
            })
            chunk_index += 1
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


def ingest_all():
    documents = load_documents()
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc)
        all_chunks.extend(chunks)
    print(f"Total chunks created: {len(all_chunks)}")
    return all_chunks