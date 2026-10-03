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

DEFAULT_MODEL_NAME  = "llama3.2:3b"
DEFAULT_TEMPERATURE = 0.2   # lower = more consistent wording
DEFAULT_NUM_PREDICT = 300   # raised — responses are now 4-6 sentences (60-120 words)
DEFAULT_NUM_CTX     = 1800  # fits few-shot prompt + RAG context + response


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
        model_name:   Ollama model installed locally.
        temperature:  Randomness of output (lower = more consistent).
        num_predict:  Max tokens to generate.
                      250 prevents mid-sentence cut-off for 3-4 sentence
                      responses while staying reasonable on CPU.
        num_ctx:      Context window fed to Ollama.
        **kwargs:     Additional ChatOllama parameters.

    Returns:
        ChatOllama instance ready for inference.
    """
    return ChatOllama(
        model=model_name,
        temperature=temperature,
        num_predict=num_predict,
        num_ctx=num_ctx,
        stop=["Human:", "User:", "Assistant:", "\n\n\n"],
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