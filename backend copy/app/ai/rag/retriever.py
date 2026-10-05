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

# Used when search_type == "similarity"
DEFAULT_SEARCH_KWARGS = {"k": 4}

# Used when search_type == "mmr"
# fetch_k  : candidate pool size before MMR re-ranking
# lambda_mult : diversity weight (0 = max diversity, 1 = max relevance)
DEFAULT_MMR_SEARCH_KWARGS = {"k": 4, "fetch_k": 8, "lambda_mult": 0.5}


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
            Type of search.
            ``"similarity"`` — standard cosine/dot-product retrieval.
            ``"mmr"``        — Maximum Marginal Relevance retrieval,
                               which balances relevance with diversity.
            Defaults to ``"similarity"``.
        search_kwargs:
            Extra search options.
            For ``"similarity"``: ``{"k": 4}`` (default).
            For ``"mmr"``: ``{"k": 4, "fetch_k": 8, "lambda_mult": 0.5}``
            (default). Pass an explicit dict to override any value.

    Returns:
        A ready-to-use retriever object. Chunk retrieval only —
        no LLM, no QA.
    """

    # Pick the right defaults when the caller passes nothing
    if search_kwargs is None:
        if search_type == "mmr":
            search_kwargs = DEFAULT_MMR_SEARCH_KWARGS
        else:
            search_kwargs = DEFAULT_SEARCH_KWARGS

    # Simple log so every run shows which retrieval mode is active
    print(f"[Retriever] search_type={search_type}  search_kwargs={search_kwargs}")

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

    print(f"Default search type        : {DEFAULT_SEARCH_TYPE}")
    print(f"Default similarity kwargs  : {DEFAULT_SEARCH_KWARGS}")
    print(f"Default MMR kwargs         : {DEFAULT_MMR_SEARCH_KWARGS}")
    print("Retriever factory ready (requires a vector store).")

