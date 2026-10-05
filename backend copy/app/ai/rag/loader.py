"""
=========================================================
RAG Document Loader
Project : AI Mental Health Chatbot (FYP)

Modular document loading layer for the RAG knowledge base.

- Scans every PDF under ``backend/knowledge_base/pdfs``
  recursively (no hardcoded file names; new PDFs are
  detected automatically).
- Reads web URLs from ``backend/knowledge_base/web_urls/urls.txt``
  (blank lines and lines starting with ``#`` are ignored).
- Returns LangChain ``Document`` objects ready for
  chunking / embedding.
=========================================================
"""

from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document

# -------------------------------------------------------
# Knowledge Base Paths (Cross Platform)
# -------------------------------------------------------

# backend/  (parents[3] of .../app/ai/rag/loader.py)
BACKEND_DIR = Path(__file__).resolve().parents[3]

# backend/knowledge_base/
KNOWLEDGE_BASE_DIR = BACKEND_DIR / "knowledge_base"

# backend/knowledge_base/pdfs/
PDFS_DIR = KNOWLEDGE_BASE_DIR / "pdfs"

# backend/knowledge_base/web_urls/urls.txt
URLS_FILE = KNOWLEDGE_BASE_DIR / "web_urls" / "urls.txt"


# =====================================================
# PDF Loading
# =====================================================

def load_pdf_documents(pdfs_directory: Path = PDFS_DIR) -> List[Document]:
    """
    Load every PDF found recursively under the given directory.

    Each PDF is loaded with a LangChain ``PyPDFLoader`` and produces
    one ``Document`` per page. The source path is attached to the
    document metadata for traceability.

    Future PDFs dropped into the folder are picked up automatically
    on the next run — no code changes required.

    Args:
        pdfs_directory:
            Root folder scanned recursively for ``*.pdf`` files.
            Defaults to ``backend/knowledge_base/pdfs``.

    Returns:
        A list of LangChain ``Document`` objects.

    Raises:
        FileNotFoundError:
            If ``pdfs_directory`` does not exist.
    """

    if not pdfs_directory.exists():
        raise FileNotFoundError(
            f"PDF directory not found: {pdfs_directory}"
        )

    # Recursively collect all PDF files (case-insensitive suffix).
    pdf_files = sorted(
        path
        for path in pdfs_directory.rglob("*")
        if path.is_file() and path.suffix.lower() == ".pdf"
    )

    documents: List[Document] = []

    for pdf_path in pdf_files:
        try:
            loader = PyPDFLoader(str(pdf_path))
            loaded = loader.load()
            documents.extend(loaded)
            print(f"Loaded PDF: {pdf_path.name} ({len(loaded)} pages)")
        except Exception as exc:  # keep the pipeline alive for bad files
            print(f"Skipping PDF (failed to parse): {pdf_path} -> {exc}")

    return documents


# =====================================================
# Web URL Loading
# =====================================================

def load_web_documents(urls_file: Path = URLS_FILE) -> List[Document]:
    """
    Load documents from the URLs listed in ``urls.txt``.

    Rules applied while reading the file:
        - Blank lines are skipped.
        - Lines beginning with ``#`` are treated as comments.
        - ``#`` after a URL starts an inline comment (striped).

    Args:
        urls_file:
            Text file with one URL per line.
            Defaults to ``backend/knowledge_base/web_urls/urls.txt``.

    Returns:
        A list of LangChain ``Document`` objects fetched from the
        web pages via ``WebBaseLoader``.

    Raises:
        FileNotFoundError:
            If ``urls_file`` does not exist.
    """

    if not urls_file.exists():
        raise FileNotFoundError(
            f"URLs file not found: {urls_file}"
        )

    urls = _read_urls(urls_file)

    if not urls:
        print(f"No URLs to load in: {urls_file}")
        return []

    documents: List[Document] = []

    for url in urls:
        try:
            loader = WebBaseLoader(web_path=url)
            loaded = loader.load()
            documents.extend(loaded)
            print(f"Loaded URL: {url} ({len(loaded)} documents)")
        except Exception as exc:  # keep the pipeline alive for bad URLs
            print(f"Skipping URL (failed to fetch): {url} -> {exc}")

    return documents


def _read_urls(urls_file: Path) -> List[str]:
    """
    Read and sanitize URLs from a text file.

    Lines are trimmed, blank lines are ignored, and anything after
    a ``#`` character is treated as an inline comment.

    Args:
        urls_file: Path to the URL list file.

    Returns:
        A list of cleaned URL strings.
    """

    urls: List[str] = []

    for raw_line in urls_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if line:
            urls.append(line)

    return urls


# =====================================================
# Combined Loading
# =====================================================

def load_all_documents(
    pdfs_directory: Path = PDFS_DIR,
    urls_file: Path = URLS_FILE,
) -> List[Document]:
    """
    Load all knowledge base documents (PDFs + web URLs).

    This is the main entry point used by the RAG pipeline.

    Args:
        pdfs_directory:
            Root folder scanned recursively for PDFs.
        urls_file:
            Text file containing the web URLs.

    Returns:
        A single combined list of LangChain ``Document`` objects.
    """

    pdf_documents = load_pdf_documents(pdfs_directory)
    web_documents = load_web_documents(urls_file)

    return pdf_documents + web_documents


# =====================================================
# Command Line Mode
# =====================================================

if __name__ == "__main__":

    print("==============================")
    print("RAG Document Loader")
    print("==============================")

    docs = load_all_documents()

    print("------------------------------")
    print(f"Total documents loaded: {len(docs)}")
    print("------------------------------")

