
"""
=========================================================
RAG Pipeline
Project : AI Mental Health Chatbot (FYP)

Wires together the RAG components into a modular flow:

    Load existing knowledge-base documents
        +
    Load CounselChat documents
        ->
    Combine documents
        ->
    Split documents
        ->
    Generate embeddings
        ->
    Create FAISS vector store
        ->
    Save vector store
        ->
    Return retriever

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

from app.ai.counsel_chat.rag_documents import load_counsel_chat_documents

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
        A list of chunked LangChain Document objects.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_documents(documents)

    print(
        f"Split {len(documents)} documents into "
        f"{len(chunks)} chunks."
    )

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

    Process:
        documents
        -> split
        -> FAISS vector store
        -> retriever

    Args:
        documents:
            Raw LangChain documents.

        embeddings:
            Embedding model.

        chunk_size:
            Chunk size. Defaults to 500.

        chunk_overlap:
            Chunk overlap. Defaults to 100.

        search_type:
            Retriever search type.
            "similarity" or "mmr".

        search_kwargs:
            Retriever search settings.

    Returns:
        A ready-to-use retriever object.
    """

    # 1. Split documents into chunks.
    chunks = split_documents(
        documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    # 2. Create FAISS vector store.
    vector_store = create_vector_store(
        documents=chunks,
        embeddings=embeddings,
    )

    # 3. Create and return retriever.
    return get_retriever(
        vector_store=vector_store,
        search_type=search_type,
        search_kwargs=search_kwargs,
    )


# =====================================================
# End-to-End Pipeline
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
    End-to-end RAG pipeline.

    Process:

        1. Load PDFs + web documents
        2. Load CounselChat documents
        3. Combine all documents
        4. Split documents into chunks
        5. Generate embeddings
        6. Create FAISS vector store
        7. Save vector store
        8. Return retriever

    Notes:
        This function always creates a fresh vector store.

        It does NOT automatically load an existing vector store.
        To reuse an existing store, use load_vector_store().
    """

    # -------------------------------------------------
    # 1. Load existing knowledge-base documents
    # -------------------------------------------------

    print("=" * 60)
    print("Loading existing knowledge-base documents...")
    print("=" * 60)

    documents = load_all_documents(
        pdfs_directory=pdfs_directory,
        urls_file=urls_file,
    )

    print(
        f"Existing knowledge-base documents: {len(documents)}"
    )

    # -------------------------------------------------
    # 2. Load CounselChat documents
    # -------------------------------------------------

    print("\n" + "=" * 60)
    print("Loading CounselChat documents...")
    print("=" * 60)

    counsel_documents = load_counsel_chat_documents()

    print(
        f"CounselChat documents: {len(counsel_documents)}"
    )

    # -------------------------------------------------
    # 3. Combine all knowledge sources
    # -------------------------------------------------

    documents.extend(counsel_documents)

    print("\n" + "=" * 60)
    print(
        f"Total combined documents: {len(documents)}"
    )
    print("=" * 60)

    # -------------------------------------------------
    # 4. Split documents into chunks
    # -------------------------------------------------

    print("\nSplitting documents...")

    chunks = split_documents(
        documents,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    # -------------------------------------------------
    # 5. Generate embeddings
    # -------------------------------------------------

    print("\nLoading embedding model...")

    embeddings = get_embedding_model()

    print("Embedding model ready.")

    # -------------------------------------------------
    # 6. Create FAISS vector store
    # -------------------------------------------------

    print("\nCreating FAISS vector store...")

    vector_store = create_vector_store(
        documents=chunks,
        embeddings=embeddings,
    )

    # -------------------------------------------------
    # 7. Save FAISS vector store
    # -------------------------------------------------

    print("\nSaving vector store...")

    save_vector_store(
        vector_store=vector_store,
        store_directory=vector_store_directory,
    )

    # -------------------------------------------------
    # 8. Return retriever
    # -------------------------------------------------

    print("\nCreating retriever...")

    retriever = get_retriever(
        vector_store=vector_store,
        search_type=search_type,
        search_kwargs=search_kwargs,
    )

    print("\n" + "=" * 60)
    print("RAG Pipeline completed successfully!")
    print("=" * 60)

    return retriever


# =====================================================
# Command Line Mode
# =====================================================

if __name__ == "__main__":

    print("=" * 60)
    print("RAG Pipeline")
    print("=" * 60)

    retriever = run_pipeline()

    print("\n" + "-" * 60)
    print("Pipeline complete. Retriever ready.")
    print("-" * 60)

