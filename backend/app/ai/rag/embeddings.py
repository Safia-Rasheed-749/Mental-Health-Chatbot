"""
=========================================================
RAG Embeddings Module
Project : AI Mental Health Chatbot (FYP)

Reusable HuggingFace embedding model factory for the RAG
knowledge base.

The model name is configurable and defaults to a lightweight
sentence-transformer model. No model paths are hardcoded —
pass any HuggingFace sentence-transformer identifier.
=========================================================
"""

from langchain_huggingface import HuggingFaceEmbeddings

# -------------------------------------------------------
# Defaults (single place to change)
# -------------------------------------------------------

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_ENCODE_KWARGS = {"normalize_embeddings": True}


# =====================================================
# Embedding Model Factory
# =====================================================

def get_embedding_model(
    model_name: str = DEFAULT_EMBEDDING_MODEL,
    encode_kwargs: dict = None,
    **kwargs,
) -> HuggingFaceEmbeddings:
    """
    Create and return a HuggingFace embedding model.

    The model identifier is configurable so different sentence
    transformer models can be swapped in without code changes.

    Args:
        model_name:
            HuggingFace sentence-transformer model identifier.
            Defaults to ``all-MiniLM-L6-v2``.
        encode_kwargs:
            Keyword arguments forwarded to ``encode()``.
            Defaults to normalized embeddings for FAISS cosine
            similarity.
        **kwargs:
            Extra keyword arguments passed to
            ``HuggingFaceEmbeddings`` (e.g. ``cache_folder``,
            ``model_kwargs``, ``multi_process``).

    Returns:
        A ready-to-use ``HuggingFaceEmbeddings`` instance.
    """

    if encode_kwargs is None:
        encode_kwargs = DEFAULT_ENCODE_KWARGS

    return HuggingFaceEmbeddings(
        model_name=model_name,
        encode_kwargs=encode_kwargs,
        **kwargs,
    )


# =====================================================
# Command Line Mode
# =====================================================

if __name__ == "__main__":

    print("==============================")
    print("RAG Embeddings Module")
    print("==============================")

    embedding_model = get_embedding_model()

    print(f"Embedding model : {DEFAULT_EMBEDDING_MODEL}")
    print("Embedding model created successfully.")

