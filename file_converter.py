from __future__ import annotations

import hashlib
import re
import unicodedata
from pathlib import Path

import pymupdf4llm
from langchain_core.documents import Document

from schemas import LoadedFile

HEADER_KEYS = ["h1", "h2", "h3", "h4", "h5", "h6"]
_MD_ESCAPE_RE = re.compile(r"\\([\\`*_{}\[\]()#+\-.!|<>~])")   # "1\." -> "1."
_HEADER_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u00ad", "")
    text = _MD_ESCAPE_RE.sub(r"\1", text)          # drop markdown backslash escapes
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    text = re.sub(r"(?<=\S)[ \t]+", " ", text)   # collapse inner spaces, keep indentation
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _clean_heading(text: str) -> str:
    return re.sub(r"[*_`]+", "", _MD_ESCAPE_RE.sub(r"\1", text)).strip()


_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_SETEXT_RE = re.compile(r"^\s*(=+|-+)\s*$")          # "Title\n=====" / "Title\n-----"
_FRONT_MATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)


def _split_markdown(
    text: str,
    page: int | None,
    stack: dict[str, str],
    sections: list[Document],
) -> dict[str, str]:
    """Append heading-delimited sections of `text` to `sections`.

    `stack` holds the currently open headings ({"h1": ..., "h2": ...}); the updated
    stack is returned so the caller can carry it into the next page.
    """
    buf: list[str] = []
    in_fence = False

    def flush() -> None:
        body = "\n".join(buf).strip()
        if body:
            meta = {**stack, **({"page": page} if page is not None else {})}
            sections.append(Document(page_content=body, metadata=meta))
        buf.clear()

    def open_heading(level: int, title: str) -> None:
        nonlocal stack
        flush()
        stack = {k: v for k, v in stack.items() if HEADER_KEYS.index(k) < level}
        stack[HEADER_KEYS[level]] = title

    for line in text.splitlines():
        if _FENCE_RE.match(line):           # "# comment" inside a code block is not a heading
            in_fence = not in_fence
            buf.append(line)
            continue
        if not in_fence:
            m = _HEADER_RE.match(line)
            if m and _clean_heading(m.group(2)):
                open_heading(len(m.group(1)) - 1, _clean_heading(m.group(2)))
                continue
            m = _SETEXT_RE.match(line)
            if m and buf and buf[-1].strip() and not buf[-1].lstrip().startswith(("|", "-", "*")):
                title = _clean_heading(buf.pop())
                open_heading(0 if m.group(1)[0] == "=" else 1, title)
                continue
        buf.append(line)
    flush()
    return stack


def load_pdf(path: Path) -> list[Document]:
    """PDF -> markdown per page; the heading stack is carried across page breaks
    (a heading at the bottom of page N applies to page N+1)."""
    stack: dict[str, str] = {}
    sections: list[Document] = []
    for i, page in enumerate(pymupdf4llm.to_markdown(str(path), page_chunks=True)):
        meta = page.get("metadata", {})
        page_no = meta.get("page_number") or meta.get("page") or i + 1
        stack = _split_markdown(page.get("text", ""), page_no, stack, sections)
    return sections


def split_markdown_text(text: str) -> list[Document]:
    text = _FRONT_MATTER_RE.sub("", text.lstrip("\ufeff").replace("\r\n", "\n"))  # BOM, front matter
    sections: list[Document] = []
    _split_markdown(text, None, {}, sections)                      # markdown has no pages
    return sections


def load_markdown(path: Path) -> list[Document]:
    return split_markdown_text(path.read_text(encoding="utf-8", errors="replace"))


LOADERS = {".pdf": load_pdf, ".md": load_markdown, ".markdown": load_markdown}
FILE_TYPES = {".pdf": "pdf", ".md": "md", ".markdown": "md"}


def make_loaded_file(raw_sections: list[Document], source: str, file_type: str) -> LoadedFile:
    sections = []
    for d in raw_sections:
        text = clean_text(d.page_content)
        if not text:
            continue
        meta = {k: v for k, v in d.metadata.items() if k in HEADER_KEYS or k == "page"}
        sections.append(Document(page_content=text, metadata=meta))

    full = "\n\n".join(s.page_content for s in sections)
    return LoadedFile(
        source=source,
        file_type=file_type,
        content_hash=hashlib.sha256(full.encode("utf-8")).hexdigest(),
        sections=sections,
    )


def load_document(path: str | Path) -> LoadedFile | None:
    path = Path(path)
    loader = LOADERS.get(path.suffix.lower())
    if loader is None:
        return None
    return make_loaded_file(loader(path), str(path), FILE_TYPES[path.suffix.lower()])


def load_markdown_string(text: str, source: str) -> LoadedFile:
    """For documents that are not files on disk, e.g. an old version read from git."""
    return make_loaded_file(split_markdown_text(text), source, "md")
