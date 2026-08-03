"""
=========================================================
RAG Vector Store (FAISS)
Project : AI Mental Health Chatbot (FYP)

FAISS vector store management for the RAG knowledge base.

- ``create_vector_store`` builds a new FAISS index from documents.
- ``save_vector_store`` persists the index and metadata to disk.
- ``load_vector_store`` restores a previously saved index.
- ``vector_store_exists`` checks whether a saved index is present.

Vectors are persisted inside ``backend/knowledge_base/vector_store`` —
outside the application code, keeping data separate from code.
The store is rebuildable by re-running the create/save flow.
=========================================================
"""

from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from .loader import KNOWLEDGE_BASE_DIR

# -------------------------------------------------------
# Vector Store Location (Cross Platform)
# -------------------------------------------------------

# backend/knowledge_base/vector_store/
VECTOR_STORE_DIR = KNOWLEDGE_BASE_DIR / "vector_store"

# Index files written by FAISS inside the directory above.
INDEX_FILENAME = "index.faiss"
STORE_FILENAME = "index.pkl"


# =====================================================
# Create
# =====================================================

def create_vector_store(
    documents: List[Document],
    embeddings: Embeddings,
) -> FAISS:
    """
    Build a new FAISS vector store from the given documents.

    Args:
        documents:
            LangChain documents (already chunked if desired).
        embeddings:
            Embedding model (see ``embeddings.get_embedding_model``).

    Returns:
        An in-memory ``FAISS`` vector store. Call
        ``save_vector_store`` afterwards to persist it.
    """

    if not documents:
        raise ValueError("Cannot create a vector store from an empty document list.")

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings,
    )

    print(f"Created FAISS vector store with {len(documents)} documents.")
    return vector_store


# =====================================================
# Save
# =====================================================

def save_vector_store(
    vector_store: FAISS,
    store_directory: Path = VECTOR_STORE_DIR,
) -> Path:
    """
    Persist a FAISS vector store to ``knowledge_base/vector_store``.

    Args:
        vector_store:
            The ``FAISS`` instance to save.
        store_directory:
            Target directory. Defaults to
            ``backend/knowledge_base/vector_store``.

    Returns:
        The path to the saved directory.
    """

    store_directory.mkdir(parents=True, exist_ok=True)

    vector_store.save_local(
        folder_path=str(store_directory),
        index_name="index",
    )

    print(f"Vector store saved to: {store_directory}")
    return store_directory


# =====================================================
# Load
# =====================================================

def load_vector_store(
    embeddings: Embeddings,
    store_directory: Path = VECTOR_STORE_DIR,
) -> FAISS:
    """
    Load a previously saved FAISS vector store from disk.

    Args:
        embeddings:
            The same embedding model used when the store was created.
        store_directory:
            Source directory. Defaults to
            ``backend/knowledge_base/vector_store``.

    Returns:
        The restored ``FAISS`` vector store.

    Raises:
        FileNotFoundError:
            If a saved store does not exist in ``store_directory``.
    """

    if not vector_store_exists(store_directory):
        raise FileNotFoundError(
            f"No saved vector store found in: {store_directory}. "
            "Run the create + save flow first."
        )

    vector_store = FAISS.load_local(
        folder_path=str(store_directory),
        embeddings=embeddings,
        index_name="index",
        allow_dangerous_deserialization=True,
    )

    print(f"Loaded vector store from: {store_directory}")
    return vector_store


# =====================================================
# Helper
# =====================================================

def vector_store_exists(store_directory: Path = VECTOR_STORE_DIR) -> bool:
    """
    Check whether a saved FAISS index is present on disk.

    Args:
        store_directory:
            Target directory. Defaults to
            ``backend/knowledge_base/vector_store``.

    Returns:
        ``True`` if both required FAISS files exist.
    """

    index_file = store_directory / INDEX_FILENAME
    store_file = store_directory / STORE_FILENAME

    return index_file.exists() and store_file.exists()


# =====================================================
# Command Line Mode
# =====================================================

if __name__ == "__main__":

    from .embeddings import get_embedding_model

    print("==============================")
    print("RAG Vector Store Module")
    print("==============================")

    print(f"Vector store directory : {VECTOR_STORE_DIR}")
    print(f"Store exists           : {vector_store_exists()}")
    print("Creating embedding model (cache only)...")

    embeddings = get_embedding_model()
    print("Embedding model ready.")

