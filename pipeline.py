from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from chunker import chunk_document
from embedding import keyword_search, to_documents
from file_converter import load_document
from metadata import PROVIDERS, MetadataAgent, build_document_metadata
from schemas import Chunk, DocumentMetadata

log = logging.getLogger(__name__)


def process_file(path: str | Path, agent: MetadataAgent) -> tuple[DocumentMetadata, list[Chunk]] | None:
    if not Path(path).is_file():
        log.warning("File not found: %s (if the path contains spaces, wrap it in quotes)", path)
        return None
    doc = load_document(path)
    if doc is None:
        log.warning("Unsupported file type: %s", path)
        return None

    doc_id = doc.content_hash[:16]
    chunks = chunk_document(doc.sections, doc_id)
    llm_meta = agent.document_metadata(doc)   # 1 LLM call per document
    agent.enrich_chunks(chunks, llm_meta)     # 1 LLM call per `batch_size` chunks
    return build_document_metadata(doc, llm_meta, doc_id, len(chunks)), chunks


def save_json(doc_meta: DocumentMetadata, chunks: list[Chunk], out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{Path(doc_meta.source).stem}.{doc_meta.doc_id}.json"
    out.write_text(json.dumps(
        {"document": doc_meta.model_dump(), "chunks": [c.model_dump() for c in chunks]},
        ensure_ascii=False, indent=2,
    ), encoding="utf-8")
    return out


def expand_paths(paths: list[str]) -> list[Path]:
    """Files are kept as is; folders are searched recursively for supported files."""
    from file_converter import LOADERS
    out: list[Path] = []
    # strip stray spaces/quotes that sneak in when paths are copy-pasted
    for p in (Path(s.strip().strip("\"'").strip()) for s in paths):
        if p.is_dir():
            out += sorted(f for f in p.rglob("*") if f.is_file() and f.suffix.lower() in LOADERS)
        else:
            out.append(p)
    return out


def main() -> None:
    p = argparse.ArgumentParser(description="PDF/Markdown -> chunks + LLM metadata")
    p.add_argument("files", nargs="+", help="PDF/.md files or folders to process")
    p.add_argument("--out", default="output", help="directory for JSON results")
    p.add_argument("--provider", default="deepseek", choices=list(PROVIDERS),
                   help="deepseek (direct), orcarouter, or openrouter (NVIDIA Nemotron by default)")
    p.add_argument("--model", default=None,
                   help="model id (default depends on --provider)")
    p.add_argument("--concurrency", type=int, default=2, help="parallel LLM calls")
    p.add_argument("--search", default=None, help="after processing, run this keyword (BM25) query over the chunks")
    args = p.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    for noisy in ("httpx", "openai", "langchain_openai"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    agent = MetadataAgent(provider=args.provider, model=args.model, max_concurrency=args.concurrency)
    docs = []
    for f in expand_paths(args.files):
        result = process_file(f, agent)
        if result is None:
            continue
        doc_meta, chunks = result
        out = save_json(doc_meta, chunks, Path(args.out))
        enriched = sum(c.summary is not None for c in chunks)
        print(f"\n{f}\n  title: {doc_meta.title}\n  type/lang: {doc_meta.doc_type}/{doc_meta.language}"
              f"\n  chunks: {len(chunks)} (enriched by LLM: {enriched})\n  saved: {out}")
        docs += to_documents(chunks, doc_meta)

    if args.search and docs:
        print(f"\nTop matches for: {args.search!r}")
        for rank, doc in enumerate(keyword_search(docs, args.search, k=3), 1):
            m = doc.metadata
            page = f" | page {m['page']}" if m["page"] >= 0 else ""
            print(f"  {rank}. {m['title']} | {m['heading_path'] or '-'}{page}")
            print(f"      {m['raw_text'][:200].replace(chr(10), ' ')}...")

if __name__ == "__main__":
    main()
