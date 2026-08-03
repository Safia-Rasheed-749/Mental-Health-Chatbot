"""
=========================================================
RAG Retriever
Project : AI Mental Health Chatbot (FYP)

Builds a configurable retriever from a FAISS vector store.

This module only handles *retrieval* — it does not perform
question answering, prompt engineering, or LLM inference.
=========================================================
"""

from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import VectorStoreRetriever

# -------------------------------------------------------
# Defaults (single place to change)
# -------------------------------------------------------

DEFAULT_SEARCH_TYPE = "similarity"
DEFAULT_SEARCH_KWARGS = {"k": 4}


# =====================================================
# Retriever Factory
# =====================================================

def get_retriever(
    vector_store: FAISS,
    search_type: str = DEFAULT_SEARCH_TYPE,
    search_kwargs: dict = None,
) -> VectorStoreRetriever:
    """
    Create a retriever from a vector store.

    The search behaviour is configurable through ``search_type``
    and ``search_kwargs``.

    Args:
        vector_store:
            A FAISS vector store (created or loaded).
        search_type:
            Type of search. Supported values include
            ``"similarity"`` and ``"mmr"``.
            Defaults to ``"similarity"``.
        search_kwargs:
            Extra search options, e.g. ``{"k": 4}``.
            Defaults to ``{"k": 4}``.

    Returns:
        A ready-to-use retriever object. Chunk retrieval only —
        no LLM, no QA.
    """

    if search_kwargs is None:
        search_kwargs = DEFAULT_SEARCH_KWARGS

    return vector_store.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs,
    )


# =====================================================
# Command Line Mode
# =====================================================

if __name__ == "__main__":

    print("==============================")
    print("RAG Retriever Module")
    print("==============================")

    print(f"Default search type : {DEFAULT_SEARCH_TYPE}")
    print(f"Default search kwargs : {DEFAULT_SEARCH_KWARGS}")
    print("Retriever factory ready (requires a vector store).")

