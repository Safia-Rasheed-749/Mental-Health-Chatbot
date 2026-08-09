"""
=========================================================
LLM Test Script
Project : AI Mental Health Chatbot (FYP)

Standalone testing utility for the local ``Llama 3.2 1B`` model.

This script ONLY tests the local LLM:
    - Creates the ``ChatOllama`` instance via ``get_llm()``.
    - Sends a single simple test message to the model.
    - Prints the model's response clearly.
    - Confirms the local LLM is reachable and generating.

It does NOT:
    - Integrate the RAG retriever.
    - Build any prompt or chain.
    - Modify the knowledge base.
    - Modify the vector store.

Requirements before running:
    - ``Ollama`` must be running locally.
    - The ``llama3.2:1b`` model must be pulled locally.

Run it from the ``backend`` directory:

    python -m app.ai.llm.test_llm
=========================================================
"""

from .llm import get_llm

# -------------------------------------------------------
# Defaults (single place to change)
# -------------------------------------------------------

TEST_MESSAGE = (
    "Hello. Please introduce yourself in one sentence and tell me "
    "how a mental health assistant can support users."
)


# =====================================================
# Test Orchestration
# =====================================================

def run_llm_test() -> None:
    """
    Create the local LLM and send it a single test message.

    Prints a clear status message on success, and clear, actionable
    error messages if the LLM is unavailable (Ollama not running) or
    the model is not installed. Errors are surfaced, never swallowed
    silently.
    """

    print("==============================")
    print("LOCAL LLM TEST")
    print("==============================")

    # 1. Create the configured ChatOllama instance.
    print("\nCreating local LLM instance ...")

    try:
        llm = get_llm()
    except Exception as exc:
        print(f"\n[ERROR] Failed to create the LLM instance: {exc}")
        print(
            "Check that the `langchain-ollama` package is installed "
            "and that the code matches the existing llm.py factory."
        )
        return

    print("LLM instance created successfully.")

    # 2. Send a single test message.
    print(f"\nSending test message ...\n> {TEST_MESSAGE}\n")

    try:
        response = llm.invoke(TEST_MESSAGE)
    except ConnectionError as exc:
        print(f"\n[ERROR] Could not reach Ollama: {exc}")
        print(
            "Is Ollama running? Start the Ollama application/shortcut "
            "and then try again."
        )
        return
    except Exception as exc:
        error_text = str(exc)
        if "not found" in error_text or "pull" in error_text.lower():
            print(f"\n[ERROR] Model unavailable: {exc}")
            print(
                "The `llama3.2:1b` model may not be installed. "
                "Pull it with:  ollama pull llama3.2:1b"
            )
        else:
            print(f"\n[ERROR] LLM inference failed: {exc}")
        return

    # 3. Print the response clearly.
    content = response.content if hasattr(response, "content") else str(response)

    print("==============================")
    print("MODEL RESPONSE")
    print("==============================")
    print(content)
    print("==============================")

    print("\n[OK] Local LLM is reachable and generating responses.")


# =====================================================
# Command Line Mode
# =====================================================

if __name__ == "__main__":
    run_llm_test()

