"""
=========================================================
RAG Pipeline
Project : AI Mental Health Chatbot (FYP)

Wires together the RAG components into a modular flow:

    Load documents
        -> Split documents
        -> Generate embeddings
        -> Create the vector store (requires embedding model)
        -> Return retriever

This module intentionally does NOT:
    - Make automatic create/load decisions (caller chooses).
    - Integrate any LLM.
    - Implement prompt engineering or chat responses.
    - Perform question answering.

The pipeline exposes reusable building blocks so rebuilding
the vector database is an explicit, caller-driven action.
=========================================================
"""

from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .embeddings import get_embedding_model
from .loader import (
    PDFS_DIR,
    URLS_FILE,
    load_all_documents,
)
from .retriever import get_retriever
from .vector_store import (
    VECTOR_STORE_DIR,
    create_vector_store,
    save_vector_store,
)

# -------------------------------------------------------
# Defaults (single place to change)
# -------------------------------------------------------

DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_OVERLAP = 100


# =====================================================
# Document Splitting
# =====================================================

def split_documents(
    documents: List[Document],
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> List[Document]:
    """
    Split a list of documents into smaller, overlapping chunks.

    Args:
        documents:
            LangChain documents to split.
        chunk_size:
            Target chunk size in characters.
            Defaults to 500.
        chunk_overlap:
            Overlap between adjacent chunks.
            Defaults to 100.

    Returns:
        A list of chunked LangChain ``Document`` objects.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_documents(documents)

    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks


# =====================================================
# Modular Pipeline Steps
# =====================================================

def build_retriever(
    documents: List[Document],
    embeddings: Embeddings,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    search_type: str = "similarity",
    search_kwargs: dict = None,
) -> VectorStoreRetriever:
    """
    Build a ready-to-use retriever from documents.

    This is the scaffold pipeline: split -> embed -> create the
    vector store -> return the retriever. The caller is expected
    to ``save_vector_store`` afterwards to persist the index.

    Args:
        documents:
            Raw documents (e.g. from ``load_all_documents``).
        embeddings:
            Embedding model (e.g. ``get_embedding_model``).
        chunk_size:
            Splitter chunk size. Defaults to 500.
        chunk_overlap:
            Splitter chunk overlap. Defaults to 100.
        search_type:
            Retriever search type (e.g. ``"similarity"``).
        search_kwargs:
            Retriever search options (e.g. ``{"k": 4}``).

    Returns:
        A ready-to-use retriever object.
    """

    # 1. Split documents into chunks.
    chunks = split_documents(
        documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    # 2. Create the FAISS vector store from the chunks.
    vector_store = create_vector_store(
        documents=chunks,
        embeddings=embeddings,
    )

    # 3. Return the retriever.
    return get_retriever(
        vector_store=vector_store,
        search_type=search_type,
        search_kwargs=search_kwargs,
    )


# =====================================================
# End-to-End Pipeline (explicit create/save)
# =====================================================

def run_pipeline(
    pdfs_directory: Path = PDFS_DIR,
    urls_file: Path = URLS_FILE,
    vector_store_directory: Path = VECTOR_STORE_DIR,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    search_type: str = "similarity",
    search_kwargs: dict = None,
) -> VectorStoreRetriever:
    """
    End-to-end convenience pipeline: load -> split -> embed -> create.

    Note: this pipeline always *creates* a fresh vector store. It does
    NOT automatically load an existing one — the caller decides when
    to rebuild vs. reuse. To reuse an existing index, call
    ``load_vector_store`` directly.

    Args:
        pdfs_directory:
            Root folder scanned recursively for PDFs.
        urls_file:
            Text file containing web URLs.
        vector_store_directory:
            Where to save the built vector store.
        chunk_size:
            Splitter chunk size. Defaults to 500.
        chunk_overlap:
            Splitter chunk overlap. Defaults to 100.
        search_type:
            Retriever search type.
        search_kwargs:
            Retriever search options.

    Returns:
        A ready-to-use retriever object.
    """

    # 1. Load documents.
    documents = load_all_documents(
        pdfs_directory=pdfs_directory,
        urls_file=urls_file,
    )

    # 2. Split documents.
    chunks = split_documents(
        documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    # 3. Generate embeddings.
    embeddings = get_embedding_model()

    # 4. Create the vector store.
    vector_store = create_vector_store(
        documents=chunks,
        embeddings=embeddings,
    )

    # 5. Persist the vector store.
    save_vector_store(
        vector_store=vector_store,
        store_directory=vector_store_directory,
    )

    # 6. Return the retriever.
    return get_retriever(
        vector_store=vector_store,
        search_type=search_type,
        search_kwargs=search_kwargs,
    )


# =====================================================
# Command Line Mode
# =====================================================

if __name__ == "__main__":

    print("==============================")
    print("RAG Pipeline")
    print("==============================")

    retriever = run_pipeline()

    print("------------------------------")
    print("Pipeline complete. Retriever ready.")
    print("------------------------------")
