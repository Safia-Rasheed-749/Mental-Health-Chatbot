"""Rebuild the FAISS knowledge-base index from PDFs and configured URLs."""

from pathlib import Path
import sys

from langchain_text_splitters import RecursiveCharacterTextSplitter


# Make the backend package importable when this file is run directly from
# ``backend/scripts`` (without importing the full RAG pipeline).
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.ai.rag.embeddings import get_embedding_model
from app.ai.rag.loader import load_pdf_documents, load_web_documents
from app.ai.rag.vector_store import (
    VECTOR_STORE_DIR,
    create_vector_store,
    save_vector_store,
)


def main() -> None:
    print("=" * 60)
    print("Rebuilding RAG vector store (PDFs + web URLs only)")
    print("=" * 60)

    pdf_documents = load_pdf_documents()
    web_documents = load_web_documents()
    documents = pdf_documents + web_documents

    print(f"PDF documents loaded (pages): {len(pdf_documents)}")
    print(f"Web documents loaded: {len(web_documents)}")
    print(f"Total PDF/Web documents loaded: {len(documents)}")

    if not documents:
        raise RuntimeError("No PDF or web documents were loaded; index was not overwritten.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    chunks = splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")

    embeddings = get_embedding_model()
    vector_store = create_vector_store(chunks, embeddings)
    save_vector_store(vector_store, VECTOR_STORE_DIR)

    print(f"Final FAISS vector count: {vector_store.index.ntotal}")
    print(f"Vector store saved to: {VECTOR_STORE_DIR}")


if __name__ == "__main__":
    main()
