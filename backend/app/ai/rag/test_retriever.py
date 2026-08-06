"""
=========================================================
RAG Retriever Test Script
Project : AI Mental Health Chatbot (FYP)

Standalone testing utility for the RAG retrieval layer.

This script ONLY tests retrieval:
    - Loads the existing embedding model.
    - Loads the existing FAISS vector store from disk.
    - Builds a retriever.
    - Asks the user for a question.
    - Retrieves the top-N relevant chunks.
    - Prints the chunks with source and page metadata.

It intentionally does NOT:
    - Integrate any LLM.
    - Generate answers or summaries.
    - Modify / rebuild the vector store.
    - Recreate embeddings.

Run it after ``pipeline.run_pipeline`` has built and saved the
store at least once. The full pipeline only needs to be run
again when the knowledge base changes.
=========================================================
"""

from .embeddings import get_embedding_model
from .retriever import get_retriever
from .vector_store import load_vector_store

# -------------------------------------------------------
# Defaults (single place to change)
# -------------------------------------------------------

TOP_K = 4  # Number of relevant chunks to retrieve.


# =====================================================
# Question Prompting
# =====================================================

def ask_question() -> str:
    """
    Prompt the user for a retrieval question.

    Returns:
        The question entered by the user (stripped).
    """

    print("\n" + "=" * 60)
    print("RAG RETRIEVAL TEST")
    print("=" * 60)

    return input("\nEnter your question (or press Enter to quit): ").strip()


# =====================================================
# Result Printing
# =====================================================

def print_results(documents: list, question: str) -> None:
    """
    Print the retrieved chunks with their metadata.

    Args:
        documents:
            List of retrieved LangChain ``Document`` objects.
        question:
            The question the chunks were retrieved for.
    """

    print("\n" + "=" * 60)
    print("RETRIEVED CHUNKS")
    print("=" * 60)
    print(f"Question : {question}")
    print(f"Results  : {len(documents)} chunk(s) found.")
    print("-" * 60)

    for index, document in enumerate(documents, start=1):
        _print_single_chunk(index, document)


def _print_single_chunk(index: int, document) -> None:
    """
    Print a single retrieved chunk neatly.

    Args:
        index:
            1-based chunk number.
        document:
            A retrieved LangChain ``Document``.
    """

    metadata = document.metadata or {}

    source = metadata.get("source", "Unknown source")
    page = metadata.get("page", None)

    print(f"\n--- Chunk {index} ---")
    print(f"Source : {source}")

    # Page number is only shown when the loader provides one.
    if page is not None:
        print(f"Page   : {page}")

    print(f"Content:\n{document.page_content}")
    print("-" * 60)


# =====================================================
# Main Entry Point
# =====================================================

def main() -> None:
    """
    Orchestrate the retrieval test.

    Loads the embedding model and vector store, builds the
    retriever, then loops asking the user for questions until
    they choose to quit. Each question retrieves the top-K
    most relevant chunks and prints them.
    """

    embeddings = None
    retriever = None

    try:
        print("Loading embedding model ...")
        embeddings = get_embedding_model()

        print("Loading vector store ...")
        vector_store = load_vector_store(embeddings)

        print("Building retriever ...")
        retriever = get_retriever(
            vector_store=vector_store,
            search_kwargs={"k": TOP_K},
        )

    except FileNotFoundError as exc:
        print(f"\n[ERROR] {exc}")
        print("Run the RAG pipeline first to build and save the vector store.")
        return
    except Exception as exc:
        print(f"\n[ERROR] Failed to initialise retrieval: {exc}")
        return

    while True:
        question = ask_question()

        # Empty input exits the loop.
        if not question:
            print("\nExiting retrieval test. Goodbye!")
            break

        try:
            documents = retriever.invoke(question)

            if not documents:
                print("\nNo relevant chunks found. Try rephrasing your question.")
            else:
                print_results(documents, question)

        except Exception as exc:
            print(f"\n[ERROR] Retrieval failed: {exc}")


# =====================================================
# Command Line Mode
# =====================================================

if __name__ == "__main__":
    main()