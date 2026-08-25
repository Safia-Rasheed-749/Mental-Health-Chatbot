# backend/app/services/rag_chat_service.py

"""
RAG Chat Service - Mental Health Chatbot FYP

This service integrates:
1. RAG pipeline (retrieval from knowledge base)
2. LLM (response generation using retrieved context)

Purpose: Provides chat responses grounded in the knowledge base
without diagnosing or giving medical advice.
"""

from typing import List
from langchain_core.documents import Document
from app.ai.llm.llm import get_llm
from app.ai.llm.prompt import get_prompt
from app.ai.rag.embeddings import get_embedding_model
from app.ai.rag.retriever import get_retriever
from app.ai.rag.vector_store import load_vector_store

# =====================================================
# Configuration
# =====================================================

TOP_K = 4  # Number of chunks to retrieve

# =====================================================
# Context Builder
# =====================================================

def build_context(documents: List[Document]) -> str:
    """
    Convert retrieved documents into a formatted context string.
    
    Args:
        documents: List of Document objects from retriever
        
    Returns:
        Formatted context string with chunk numbers
    """
    parts = []
    
    for index, document in enumerate(documents, start=1):
        parts.append(
            f"[Chunk {index}]\n{document.page_content}"
        )
    
    return "\n\n".join(parts)

# =====================================================
# RAG Chat Initialization
# =====================================================

def initialize_rag_chat():
    """
    Initialize all RAG components:
    1. Embedding model
    2. Vector store (FAISS)
    3. Retriever
    4. LLM
    5. Prompt template
    
    Returns:
        tuple: (retriever, llm, prompt)
    """
    print("🔍 Initializing RAG Chat Service...")
    
    # Step 1: Load embedding model
    print("  📥 Loading embedding model...")
    embeddings = get_embedding_model()
    
    # Step 2: Load vector store
    print("  📚 Loading vector store...")
    vector_store = load_vector_store(embeddings)
    
    # Step 3: Create retriever
    print(f"  🔍 Creating retriever (top_k={TOP_K})...")
    retriever = get_retriever(
        vector_store=vector_store,
        search_type="similarity",  # or "mmr" if you implemented it
        search_kwargs={"k": TOP_K},
    )
    
    # Step 4: Load LLM
    print("  🤖 Loading LLM...")
    llm = get_llm()
    
    # Step 5: Load prompt template
    print("  📝 Loading prompt template...")
    prompt = get_prompt()
    
    print("✅ RAG Chat Service initialized successfully!")
    return retriever, llm, prompt


# Initialize once when module loads
retriever, llm, prompt = initialize_rag_chat()

# =====================================================
# Main Chat Function
# =====================================================

def generate_chat_response(question: str) -> str:
    """
    Generate a response using RAG + LLM.
    
    Process:
    1. Retrieve relevant chunks from knowledge base
    2. Build context from retrieved chunks
    3. Format prompt with context and question
    4. Generate response using LLM
    
    Args:
        question: User's input/question
        
    Returns:
        str: Generated response (or error message)
    """
    print(f"💬 Generating response for: {question[:50]}...")
    
    # Step 1: Retrieve relevant documents
    documents = retriever.invoke(question)
    
    # Step 2: Check if any documents were retrieved
    if not documents:
        return (
            "I don't have enough information in my knowledge base "
            "to answer that question. Please rephrase or ask something else."
        )
    
    # Step 3: Build context from retrieved documents
    context = build_context(documents)
    
    # Step 4: Format the prompt
    messages = prompt.format_messages(
        context=context,
        question=question,
    )
    
    # Step 5: Generate response
    response = llm.invoke(messages)
    
    # Step 6: Extract content
    response_text = response.content if hasattr(response, "content") else str(response)
    
    print("✅ Response generated successfully!")
    return response_text

# =====================================================
# Helper Functions (Optional)
# =====================================================

def get_retrieved_chunks(question: str) -> List[Document]:
    """
    Helper function to inspect retrieved chunks without generating response.
    Useful for debugging and evaluation.
    
    Args:
        question: User's input/question
        
    Returns:
        List of retrieved documents
    """
    return retriever.invoke(question)


def generate_response_with_context(question: str) -> dict:
    """
    Generate response and return it with context for evaluation.
    
    Args:
        question: User's input/question
        
    Returns:
        dict: {
            "question": str,
            "response": str,
            "context": str,
            "retrieved_chunks": List[Document]
        }
    """
    documents = retriever.invoke(question)
    context = build_context(documents)
    
    messages = prompt.format_messages(
        context=context,
        question=question,
    )
    
    response = llm.invoke(messages)
    response_text = response.content if hasattr(response, "content") else str(response)
    
    return {
        "question": question,
        "response": response_text,
        "context": context,
        "retrieved_chunks": documents,
    }

# =====================================================
# Test Function (Run only if executed directly)
# =====================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Testing RAG Chat Service")
    print("=" * 60)
    
    # Test queries
    test_queries = [
        "I have been feeling really low and empty lately. Can you help me?",
        "I feel like nobody understands me and I am completely alone.",
        "I had a really bad day and I just need someone to talk to.",
    ]
    
    for query in test_queries:
        print(f"\n❓ Question: {query}")
        print("-" * 40)
        
        response = generate_chat_response(query)
        print(f"🤖 Response:\n{response}")
        print("-" * 40)