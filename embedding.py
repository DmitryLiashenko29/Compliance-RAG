from __future__ import annotations

import re

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore

from schemas import Chunk, DocumentMetadata


def to_documents(chunks: list[Chunk], doc_meta: DocumentMetadata) -> list[Document]:
    """Chunks -> LangChain Documents: the format handed to the other agents / any vector store."""
    return [c.to_document(doc_meta) for c in chunks]


def _tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())          # works for English and Russian


def keyword_search(docs: list[Document], query: str, k: int = 3) -> list[Document]:
    """BM25 keyword search - no model needed. Also searches the LLM-generated
    keywords and questions, which helps when the user's wording differs from the text."""
    from langchain_community.retrievers import BM25Retriever

    def search_text(d: Document) -> str:
        m = d.metadata
        return f"{d.page_content}\n{m.get('keywords', '')}\n{m.get('questions', '')}"

    retriever = BM25Retriever.from_texts(
        [search_text(d) for d in docs], metadatas=[d.metadata for d in docs],
        preprocess_func=_tokenize, k=k,
    )
    by_id = {(d.metadata["doc_id"], d.metadata["chunk_index"]): d for d in docs}
    return [by_id[(r.metadata["doc_id"], r.metadata["chunk_index"])] for r in retriever.invoke(query)]


def index_chunks(
    chunks: list[Chunk],
    doc_meta: DocumentMetadata,
    embeddings: Embeddings,
    store: VectorStore | None = None,
) -> VectorStore:
    """Semantic index for whoever provides an embedding model (DeepSeek has none).
    Swap InMemoryVectorStore for Chroma/Qdrant/PGVector for a persistent shared index."""
    store = store or InMemoryVectorStore(embeddings)
    docs = to_documents(chunks, doc_meta)
    store.add_documents(docs, ids=[d.id for d in docs])
    return store
