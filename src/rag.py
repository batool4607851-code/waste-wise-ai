import os
import numpy as np
import faiss

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text and text.strip():

            documents.append({
                "text": text.strip(),
                "source": os.path.basename(pdf_path),
                "page": page_number,
            })

    return documents


def chunk_text(text, chunk_size=500, overlap=100):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(
            words[start:end]
        ).strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def build_chunks(pdf_path):

    pages = extract_pdf_text(pdf_path)

    chunks = []

    for page in pages:

        page_chunks = chunk_text(
            page["text"]
        )

        for chunk in page_chunks:

            chunks.append({
                "text": chunk,
                "source": page["source"],
                "page": page["page"],
            })

    return chunks


def build_vector_index(chunks):

    if not chunks:
        raise ValueError(
            "No text chunks were found."
        )

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    embeddings = embeddings.astype(
        "float32"
    )

    index = faiss.IndexFlatIP(
        embeddings.shape[1]
    )

    index.add(embeddings)

    return model, index, chunks


def retrieve_chunks(
    query,
    model,
    index,
    chunks,
    top_k=5,
):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True,
    )

    query_embedding = query_embedding.astype(
        "float32"
    )

    scores, indices = index.search(
        query_embedding,
        min(top_k, len(chunks)),
    )

    results = []

    for score, index_position in zip(
        scores[0],
        indices[0],
    ):

        if index_position < 0:
            continue

        result = chunks[index_position].copy()

        result["score"] = float(score)

        results.append(result)

    return results
