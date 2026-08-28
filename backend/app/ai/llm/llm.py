"""
=========================================================
LLM Module (Local Chat Model)
Project : AI Mental Health Chatbot (FYP)

Reusable local LLM factory for the chatbot backend.

This module is responsible ONLY for creating and returning a
configured ChatOllama instance.
=========================================================
"""

from langchain_ollama import ChatOllama


# -------------------------------------------------------
# Defaults
# -------------------------------------------------------

DEFAULT_MODEL_NAME  = "llama3.2:1b"
DEFAULT_TEMPERATURE = 0.3
DEFAULT_NUM_PREDICT = 120   # max tokens to generate — keep short for speed
DEFAULT_NUM_CTX     = 1024  # context window — smaller = faster on CPU


# =======================================================
# LLM Factory
# =======================================================

def get_llm(
    model_name: str = DEFAULT_MODEL_NAME,
    temperature: float = DEFAULT_TEMPERATURE,
    num_predict: int = DEFAULT_NUM_PREDICT,
    num_ctx: int = DEFAULT_NUM_CTX,
    **kwargs,
) -> ChatOllama:
    """
    Create and return a configured local ChatOllama instance.

    Args:
        model_name:
            Name of the Ollama model installed locally.

        temperature:
            Controls randomness of the generated response.

        num_predict:
            Maximum tokens to generate. Kept low for speed on CPU.

        num_ctx:
            Context window size fed to Ollama.
            Smaller value = faster inference on CPU.

        **kwargs:
            Additional ChatOllama parameters.

    Returns:
        ChatOllama instance ready for inference.
    """

    return ChatOllama(
        model=model_name,
        temperature=temperature,
        num_predict=num_predict,
        num_ctx=num_ctx,
        **kwargs,
    )


# =======================================================
# Command Line Mode
# =======================================================

if __name__ == "__main__":

    print("==============================")
    print("LLM Module")
    print("==============================")

    llm = get_llm()

    print(f"Selected model   : {DEFAULT_MODEL_NAME}")
    print(f"Temperature      : {DEFAULT_TEMPERATURE}")
    print(f"Max output       : {DEFAULT_NUM_PREDICT}")
    print("LLM instance created successfully.")