"""
=========================================================
LLM Module (Local Chat Model)
Project : AI Mental Health Chatbot (FYP)

Reusable local LLM factory for the chatbot backend.

This module is responsible ONLY for creating and returning a
configured ``ChatOllama`` instance. It behaves exactly like the
embeddings module — it does NOT:

    - perform inference
    - build chains
    - retrieve documents
    - use prompts
    - generate chatbot responses

The model name and temperature are configurable so different
Ollama models can be swapped in without code changes. The
default model ``llama3.2:1b`` is a lightweight 1B model suitable
for local execution.
=========================================================
"""

from langchain_ollama import ChatOllama

# -------------------------------------------------------
# Defaults (single place to change)
# -------------------------------------------------------

DEFAULT_MODEL_NAME = "llama3.2:1b"
DEFAULT_TEMPERATURE = 0.3


# =====================================================
# LLM Factory
# =====================================================

def get_llm(
    model_name: str = DEFAULT_MODEL_NAME,
    temperature: float = DEFAULT_TEMPERATURE,
    **kwargs,
) -> ChatOllama:
    """
    Create and return a configured local ``ChatOllama`` instance.

    The model identifier and temperature are configurable so
    different Ollama models can be swapped in at run time or at
    import time without changing any code.

    This factory only builds the model object. It does not invoke
    the model, build a chain, or perform any inference.

    Args:
        model_name:
            Name of an Ollama model installed locally.
            Defaults to ``llama3.2:1b``.
        temperature:
            Sampling temperature for the model.
            Defaults to ``0.3``.
        **kwargs:
            Extra keyword arguments passed to ``ChatOllama``
            (e.g. ``base_url``, ``num_predict``, ``timeout``).

    Returns:
        A ready-to-use ``ChatOllama`` instance.
    """

    return ChatOllama(
        model=model_name,
        temperature=temperature,
        **kwargs,
    )


# =====================================================
# Command Line Mode
# =====================================================

if __name__ == "__main__":

    print("==============================")
    print("LLM Module")
    print("==============================")

    llm = get_llm()

    print(f"Selected model   : {DEFAULT_MODEL_NAME}")
    print(f"Temperature      : {DEFAULT_TEMPERATURE}")
    print("LLM instance created successfully.")
