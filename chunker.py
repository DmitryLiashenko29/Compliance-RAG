from __future__ import annotations

import re

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from file_converter import HEADER_KEYS
from schemas import Chunk


_CLAUSE_RE = re.compile(r"^(?:section|article|раздел|пункт|статья)?\s*(\d{1,3}(?:\.\d{1,3})*)[.)]?\s+(.+)$", re.I)


def find_clause(heading_path: list[str]) -> tuple[str | None, str | None]:
    """Deepest numbered heading -> ("4.2", "Refunds"); no numbering -> (None, last heading)."""
    for heading in reversed(heading_path):
        m = _CLAUSE_RE.match(heading.strip())
        if m:
            return m.group(1), m.group(2).strip()
    return None, (heading_path[-1] if heading_path else None)


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def chunk_document(
    sections: list[Document],
    doc_id: str,
    max_tokens: int = 500,
    overlap_tokens: int = 60,
) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_tokens,
        chunk_overlap=overlap_tokens,
        length_function=estimate_tokens,     # sizes in ~tokens instead of characters
        separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""],
        keep_separator="end",                # keep the "." on the sentence it ends
    )
    # NOTE: not using add_start_index - it subtracts chunk_overlap (tokens here) from a
    # character offset and returns wrong/-1 values. We compute offsets ourselves.

    chunks: list[Chunk] = []
    doc_offset = 0                           # offset of the section in LoadedFile.full_text
    for section in sections:
        text, md = section.page_content, section.metadata
        cursor, min_next = 0, 0
        for piece in splitter.split_text(text):
            # next piece starts after the previous one, overlapping it by <= ~overlap chars
            local = text.find(piece, cursor)
            if local == -1:
                local = text.find(piece, min_next)
            min_next = local + 1
            cursor = max(min_next, local + len(piece) - 2 * overlap_tokens * 4)
            i = len(chunks)
            heading_path = [md[k] for k in HEADER_KEYS if md.get(k)]
            clause, clause_title = find_clause(heading_path)
            chunks.append(Chunk(
                chunk_id=f"{doc_id}::{i:04d}",
                doc_id=doc_id,
                chunk_index=i,
                text=piece,
                heading_path=heading_path,
                clause=clause,
                clause_title=clause_title,
                page=md.get("page"),
                char_start=doc_offset + local if local >= 0 else None,  # index into full_text
                char_count=len(piece),
                token_estimate=estimate_tokens(piece),
            ))
        doc_offset += len(text) + 2          # "\n\n" separator used in full_text
    return chunks
