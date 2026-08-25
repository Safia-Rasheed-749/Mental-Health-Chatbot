"""
=========================================================
RAG + LLM Integration Test Script
Project : AI Mental Health Chatbot (FYP)

Standalone testing utility for the complete RAG answer flow:

    User question
        -> Existing FAISS retriever (top-k chunks)
        -> Prompt template (context + question)
        -> Local Llama 3.2 1B via Ollama
        -> Grounded response

This script:
    - Loads the existing embedding model.
    - Loads the existing FAISS vector store (does NOT rebuild it).
    - Builds the existing retriever with ``k=4``.
    - Gets the local LLM via ``get_llm()``.
    - Gets the prompt template from ``prompt.get_prompt()``.
    - Asks the user for a question.
    - Retrieves the top-k relevant chunks.
    - Builds the context string from the retrieved documents.
    - Sends the prompt to the local LLM.
    - Prints the question, the retrieved source documents, and the
      generated response so retrieval can be manually compared with
      the grounded answer.

It intentionally does NOT:
    - Rebuild / modify the vector store.
    - Create new embeddings.
    - Modify the knowledge base.
    - Integrate FastAPI.
    - Integrate emotion detection.
    - Modify PostgreSQL.

Requirements before running:
    - Ollama running locally with ``llama3.2:1b`` pulled.
    - An existing FAISS vector store in
      ``backend/knowledge_base/vector_store``.

Run it from the ``backend`` directory:

    python -m app.ai.llm.test_rag_llm
=========================================================
"""

from .llm import get_llm
from .prompt import get_prompt

# (Imports below are local to avoid heavy top-level loading.)
from ..rag.embeddings import get_embedding_model
from ..rag.retriever import get_retriever
from ..rag.vector_store import load_vector_store

# -------------------------------------------------------
# Defaults (single place to change)
# -------------------------------------------------------

TOP_K = 4  # Number of relevant chunks to retrieve.


# =====================================================
# Question Prompting
# =====================================================

def ask_question() -> str:
    """
    Prompt the user for a question.

    Returns:
        The question entered by the user (stripped).
    """

    print("\n" + "=" * 60)
    print("RAG + LLM INTEGRATION TEST")
    print("=" * 60)

    return input("\nEnter your question (or press Enter to quit): ").strip()


# =====================================================
# Initialisation
# =====================================================

def initialise() -> tuple:
    """
    Load all RAG + LLM components needed for the test.

    Order of initialisation:
        1. Embedding model.
        2. FAISS vector store (loaded from disk, never rebuilt).
        3. Retriever (top-k).
        4. Local LLM.
        5. Prompt template.

    Returns:
        A ``(retriever, llm, prompt)`` tuple.

    Raises:
        FileNotFoundError:
            If the saved vector store is missing.
        Exception:
            Re-raised so the caller can print a clear error.
    """

    print("\nLoading embedding model ...")
    embeddings = get_embedding_model()

    print("Loading existing FAISS vector store ...")
    vector_store = load_vector_store(embeddings)

    print("Building retriever ...")
    retriever = get_retriever(
        vector_store=vector_store,
        search_kwargs={"k": TOP_K},
    )

    print("Creating local LLM (llama3.2:1b) ...")
    llm = get_llm()

    print("Building prompt template ...")
    prompt = get_prompt()

    return retriever, llm, prompt


# =====================================================
# Context Building
# =====================================================

def build_context(documents: list) -> str:
    """
    Convert a list of retrieved documents into a single context string.

    Each chunk is labelled by its 1-based index and separated by a
    blank line so the model can distinguish between sources.

    Args:
        documents:
            List of retrieved LangChain ``Document`` objects.

    Returns:
        A single string combining all chunk contents.
    """

    parts = []

    for index, document in enumerate(documents, start=1):
        parts.append(f"[Chunk {index}]\n{document.page_content}")

    return "\n\n".join(parts)


# =====================================================
# Result Printing
# =====================================================

def print_retrieved_sources(documents: list) -> None:
    """
    Print the retrieved chunks with their source metadata.

    This is printed so the user can manually compare the retrieval
    results with the generated response (grounding check).

    Args:
        documents:
            List of retrieved LangChain ``Document`` objects.
    """

    print("\n" + "=" * 60)
    print("RETRIEVED SOURCE DOCUMENTS")
    print("=" * 60)
    print(f"Results  : {len(documents)} chunk(s) found.")
    print("-" * 60)

    for index, document in enumerate(documents, start=1):
        metadata = document.metadata or {}
        source = metadata.get("source", "Unknown source")
        page = metadata.get("page", None)

        print(f"\n--- Chunk {index} ---")
        print(f"Source : {source}")

        if page is not None:
            print(f"Page   : {page}")

        print(f"Content:\n{document.page_content}")
        print("-" * 60)


def print_generated_response(response) -> None:
    """
    Print the generated LLM response.

    Args:
        response:
            The raw response object returned by ``llm.invoke``.
    """

    content = response.content if hasattr(response, "content") else str(response)

    print("\n" + "=" * 60)
    print("GENERATED RESPONSE")
    print("=" * 60)
    print(content)
    print("=" * 60)


# =====================================================
# Main Entry Point
# =====================================================

def main() -> None:
    """
    Orchestrate the RAG + LLM integration test.

    Loads all components, then loops asking the user for questions
    until they choose to quit. Each question:
        1. Retrieves the top-k relevant chunks.
        2. Builds the context string.
        3. Invokes the local LLM with the prompt.
        4. Prints the question, the retrieved sources, and the answer.
    """

    retriever = None
    llm = None
    prompt = None

    try:
        retriever, llm, prompt = initialise()
    except FileNotFoundError as exc:
        print(f"\n[ERROR] {exc}")
        print("Run the RAG pipeline first to build and save the vector store.")
        return
    except ConnectionError as exc:
        print(f"\n[ERROR] Could not reach the local LLM: {exc}")
        print("Is Ollama running? Start Ollama and try again.")
        return
    except Exception as exc:
        error_text = str(exc)
        if "not found" in error_text or "pull" in error_text.lower():
            print(f"\n[ERROR] Model unavailable: {exc}")
            print("Pull it with:  ollama pull llama3.2:1b")
        else:
            print(f"\n[ERROR] Failed to initialise the RAG + LLM stack: {exc}")
        return

    while True:
        question = ask_question()

        # Empty input exits the loop.
        if not question:
            print("\nExiting RAG + LLM test. Goodbye!")
            break

        # 1. Retrieve the top-k relevant chunks.
        print("\nRetrieving relevant chunks ...")

        try:
            documents = retriever.invoke(question)
        except Exception as exc:
            print(f"\n[ERROR] Retrieval failed: {exc}")
            continue

        if not documents:
            print("\n[WARNING] No documents were retrieved.")
            print("Relevant context is empty; the model cannot answer reliably.")
            print("Try rephrasing your question.")
            continue

        # 2. Build the context string.
        context = build_context(documents)

        # 3. Invoke the local LLM with the prompt.
        print("Generating grounded response ...")

        try:
            messages = prompt.format_messages(
                context=context,
                question=question,
            )
            response = llm.invoke(messages)
        except ConnectionError as exc:
            print(f"\n[ERROR] Could not reach the local LLM: {exc}")
            print("Is Ollama running? Start Ollama and try again.")
            break
        except Exception as exc:
            error_text = str(exc)
            if "not found" in error_text or "pull" in error_text.lower():
                print(f"\n[ERROR] Model unavailable: {exc}")
                print("Pull it with:  ollama pull llama3.2:1b")
            else:
                print(f"\n[ERROR] LLM invocation failed: {exc}")
            break

        # 4. Print everything for manual grounding comparison.
        print("\n" + "=" * 60)
        print("USER QUESTION")
        print("=" * 60)
        print(question)

        print_retrieved_sources(documents)
        print_generated_response(response)


# =====================================================
# Command Line Mode
# =====================================================

if __name__ == "__main__":
    main()
