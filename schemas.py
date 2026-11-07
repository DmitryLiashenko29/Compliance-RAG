from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from langchain_core.documents import Document
from pydantic import BaseModel, Field

DocType = Literal[
    "terms_of_service", "privacy_policy", "community_guidelines", "policy", "contract", "manual",
    "report", "faq", "spec", "other",
]
ContentType = Literal[
    "definition", "rule", "obligation", "right", "limitation",
    "procedure", "pricing", "contact", "other",
]


# ---------- output of file_converter ----------

class LoadedFile(BaseModel):
    source: str
    file_type: str
    content_hash: str
    sections: list[Document]

    @property
    def full_text(self) -> str:
        return "\n\n".join(s.page_content for s in self.sections)


# ---------- what the LLM must return (structured output) ----------

class DocumentMetadataLLM(BaseModel):
    title: str = Field(description="Document title, as written in the document if present")
    doc_type: DocType = Field(description="Kind of document")
    language: str = Field(description="Main language of the document, ISO 639-1 code (en, ru, ...)")
    summary: str = Field(description="2-4 sentence summary of what the document covers")


class ChunkMetadataLLM(BaseModel):
    chunk_index: int = Field(description="Copy the index attribute of the chunk exactly")
    summary: str = Field(description="One sentence: what this chunk says")
    keywords: list[str] = Field(description="3-8 specific keywords/terms from the chunk")
    questions: list[str] = Field(description="2-4 user questions this chunk answers")
    content_type: ContentType = Field(description="Main type of content in the chunk")
    context: str = Field(description="One sentence situating the chunk within the whole document")


class ChunkBatchLLM(BaseModel):
    chunks: list[ChunkMetadataLLM]


# ---------- final objects handed to the other agents ----------

class DocumentMetadata(DocumentMetadataLLM):
    doc_id: str                          # unique per version: "bluesky/terms-of-service@2024-03-14_88efeaa"
    source: str
    file_type: str
    content_hash: str
    num_chunks: int
    # --- versioning (filled for the Open Terms Archive corpus, None for single files) ---
    document_key: str | None = None      # same for all versions: "bluesky/terms-of-service"
    service: str | None = None           # "Bluesky"
    document_type: str | None = None     # "Terms of Service" (Open Terms Archive name)
    version_date: str | None = None      # date the version was recorded, YYYY-MM-DD
    valid_until: str | None = None       # date the next version was recorded; None = still current
    commit: str | None = None            # git commit of this version in pga-versions
    is_latest: bool = True               # False for outdated versions
    previous_doc_id: str | None = None   # doc_id of the previous version in the index
    removed_sections: list[str] = Field(default_factory=list)  # sections dropped since the previous version
    processed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Chunk(BaseModel):
    chunk_id: str
    doc_id: str
    chunk_index: int
    text: str
    heading_path: list[str]
    page: int | None
    char_start: int | None = None
    char_count: int
    token_estimate: int
    summary: str | None = None
    keywords: list[str] = Field(default_factory=list)
    questions: list[str] = Field(default_factory=list)
    content_type: str | None = None
    context: str | None = None
    clause: str | None = None            # clause number from the headings, e.g. "3" or "4.2"
    clause_title: str | None = None      # heading of that clause, e.g. "User Content"
    # vs the previous version of the same document: "first" (no previous version),
    # "added" (new section), "changed" (section text differs), "unchanged"
    change_status: str | None = None

    def embedding_text(self, doc_title: str) -> str:
        header = f"Document: {doc_title}\nSection: {' > '.join(self.heading_path) or '-'}"
        ctx = f"\nContext: {self.context}" if self.context else ""
        return f"{header}{ctx}\n\n{self.text}"

    def flat_metadata(self) -> dict:
        # only str/int/float/bool values -> compatible with Chroma, Qdrant, FAISS, etc.
        return {
            "doc_id": self.doc_id,
            "chunk_index": self.chunk_index,
            "heading_path": " > ".join(self.heading_path),
            "page": self.page if self.page is not None else -1,
            "char_start": self.char_start if self.char_start is not None else -1,
            "summary": self.summary or "",
            "keywords": ", ".join(self.keywords),
            "questions": " | ".join(self.questions),
            "content_type": self.content_type or "",
            "clause": self.clause or "",
            "clause_title": self.clause_title or "",
            "change_status": self.change_status or "",
        }

    def to_document(self, doc_meta: DocumentMetadata) -> Document:
        return Document(
            id=self.chunk_id,
            page_content=self.embedding_text(doc_meta.title),
            metadata={
                **self.flat_metadata(),
                "raw_text": self.text,
                "title": doc_meta.title,
                "source": doc_meta.source,
                "doc_type": doc_meta.doc_type,
                "language": doc_meta.language,
                "document_key": doc_meta.document_key or doc_meta.doc_id,
                "service": doc_meta.service or "",
                "version_date": doc_meta.version_date or "",
                "valid_until": doc_meta.valid_until or "",
                "is_latest": doc_meta.is_latest,
            },
        )
