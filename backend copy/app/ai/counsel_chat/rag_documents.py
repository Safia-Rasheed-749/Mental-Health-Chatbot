"""
=========================================================
CounselChat RAG Document Builder
Project : AI Mental Health Chatbot (FYP)

Purpose:
    Convert processed CounselChat question/answer pairs
    into LangChain Document objects for the existing RAG
    pipeline.
=========================================================
"""

from pathlib import Path
from typing import List

import pandas as pd
from langchain_core.documents import Document


# =========================================================
# Paths
# =========================================================

BACKEND_DIR = Path(__file__).resolve().parents[3]

COUNSEL_CHAT_PROCESSED = (
    BACKEND_DIR
    / "datasets"
    / "counsel_chat"
    / "processed"
    / "train_processed.csv"
)


# =========================================================
# Document Builder
# =========================================================

def load_counsel_chat_documents(
    csv_path: Path = COUNSEL_CHAT_PROCESSED,
) -> List[Document]:
    """
    Load processed CounselChat data and convert each
    question/therapist-answer pair into a LangChain Document.

    Returns:
        List[Document]
    """

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Processed CounselChat dataset not found: {csv_path}"
        )

    df = pd.read_csv(csv_path)

    required_columns = [
        "questionText",
        "answerText",
        "topic",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    documents: List[Document] = []

    for index, row in df.iterrows():

        question = str(row["questionText"]).strip()
        answer = str(row["answerText"]).strip()
        topic = str(row["topic"]).strip()

        if not question or not answer:
            continue

        content = (
            f"Counseling Topic: {topic}\n\n"
            f"User Question:\n{question}\n\n"
            f"Therapist Response:\n{answer}"
        )

        metadata = {
            "source": "counsel_chat",
            "dataset": "CounselChat",
            "topic": topic,
            "row_id": int(index),
        }

        documents.append(
            Document(
                page_content=content,
                metadata=metadata,
            )
        )

    print(
        f"Loaded {len(documents)} CounselChat documents."
    )

    return documents


# =========================================================
# Test
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("CounselChat RAG Document Builder")
    print("=" * 60)

    documents = load_counsel_chat_documents()

    print(f"\nTotal Documents: {len(documents)}")

    if documents:
        print("\nSample Document")
        print("-" * 60)
        print(documents[0].page_content)

        print("\nMetadata")
        print("-" * 60)
        print(documents[0].metadata)