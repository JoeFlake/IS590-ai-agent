import os
from pathlib import Path
from typing import Optional

import chromadb
from langchain.tools import tool
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from app.logger import get_logger, log_tool_call, log_tool_error

_log = get_logger("tool.rag")

_vectorstore: Optional[Chroma] = None


def get_vectorstore() -> Chroma:
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = _build_vectorstore()
    return _vectorstore


def _chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> list:
    words = text.split()
    chunks, start = [], 0
    while start < len(words):
        chunks.append(" ".join(words[start : start + chunk_size]))
        start += chunk_size - overlap
    return chunks


def _build_vectorstore() -> Chroma:
    store = Chroma(
        client=chromadb.EphemeralClient(),
        collection_name="knowledge_base",
        embedding_function=OpenAIEmbeddings(),
    )
    docs_dir = Path(__file__).parent.parent.parent / "docs"
    documents = []
    for doc_file in list(docs_dir.glob("*.md")) + list(docs_dir.glob("*.txt")):
        text = doc_file.read_text(encoding="utf-8")
        for i, chunk in enumerate(_chunk_text(text)):
            documents.append(
                Document(page_content=chunk, metadata={"source": doc_file.name, "chunk": i})
            )
    if documents:
        store.add_documents(documents)
    return store


@tool
def rag_search(query: str) -> str:
    """Search the internal knowledge base for information about AI/ML concepts,
    Python programming, and course material. Use when the user asks about topics
    that may be covered in the documentation."""
    try:
        docs = get_vectorstore().similarity_search(query, k=3)
        if not docs:
            log_tool_call(_log, "rag_search", {"query": query}, "No results found.")
            return "No relevant documents found in the knowledge base."
        parts = [f"[Source: {d.metadata.get('source')}]\n{d.page_content}" for d in docs]
        output = "\n\n---\n\n".join(parts)
        sources = list({d.metadata.get("source") for d in docs})
        log_tool_call(_log, "rag_search", {"query": query, "sources": sources, "num_chunks": len(docs)}, output)
        return output
    except Exception as exc:
        log_tool_error(_log, "rag_search", {"query": query}, str(exc))
        return f"RAG error: {exc}"
