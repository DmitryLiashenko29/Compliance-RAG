from __future__ import annotations

import argparse
import json
import logging
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from chunker import chunk_document
from file_converter import load_markdown_string
from metadata import PROVIDERS, MetadataAgent, build_document_metadata
from schemas import Chunk, DocumentMetadata, DocumentMetadataLLM

log = logging.getLogger(__name__)

# commits that only change how the text was extracted, not the policy itself
SKIP_SUBJECTS = ("Apply technical", "Refilter")

DOC_TYPES = {
    "Terms of Service": "terms_of_service",
    "Privacy Policy": "privacy_policy",
    "Community Guidelines": "community_guidelines",
}
LLM_FIELDS = ("summary", "keywords", "questions", "content_type", "context")


@dataclass
class Version:
    commit: str
    date: str          # YYYY-MM-DD
    subject: str
    text: str | None = None


# ---------------------------------------------------------------- git helpers

def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def list_documents(repo: Path, services: list[str] | None, types: list[str] | None) -> list[str]:

    paths = [p for p in git(repo, "ls-tree", "-r", "--name-only", "-z", "HEAD").split("\0")
             if p.endswith(".md") and p.count("/") == 1]
    if services:
        wanted = {s.lower() for s in services}
        paths = [p for p in paths if p.split("/")[0].lower() in wanted]
    if types:
        wanted = {t.lower() for t in types}
        paths = [p for p in paths if Path(p).stem.lower() in wanted]
    return sorted(paths)


def list_versions(repo: Path, path: str) -> list[Version]:
    """All content commits of one document, oldest first."""
    out = git(repo, "log", "--format=%H%x1f%aI%x1f%s", "--", path)
    versions = []
    for line in out.splitlines():
        commit, date, subject = line.split("\x1f", 2)
        if not subject.startswith(SKIP_SUBJECTS):
            versions.append(Version(commit, date[:10], subject))
    return versions[::-1]


def read_text(repo: Path, v: Version, path: str) -> str:
    if v.text is None:
        v.text = git(repo, "show", f"{v.commit}:{path}")
    return v.text


def select_versions(
    repo: Path, path: str, since: str | None, until: str | None, last_n: int | None,
) -> list[tuple[Version, str | None]]:
    """Distinct versions in [since, until], keeping the newest `last_n`.

    Returns (version, valid_until) oldest first. Consecutive commits with identical text
    are merged into one version dated by the *first* of them. valid_until is the date the
    next different version appeared (None if this is still the current text).
    """
    history = list_versions(repo, path)
    in_range = [i for i, v in enumerate(history)
                if (not since or v.date >= since) and (not until or v.date <= until)]
    if not in_range:
        return []

    kept: list[int] = []                 # indexes into history, newest first
    for i in reversed(in_range):
        if kept and read_text(repo, history[i], path) == read_text(repo, history[kept[-1]], path):
            kept[-1] = i                 # same text as the newer one -> it started earlier
            continue
        if last_n and len(kept) == last_n:
            break
        kept.append(i)

    result = []
    for i in reversed(kept):
        valid_until = None
        for later in history[i + 1:]:    # first later commit with a different text
            if read_text(repo, later, path) != read_text(repo, history[i], path):
                valid_until = later.date
                break
        result.append((history[i], valid_until))
    return result


# ---------------------------------------------------------------- processing

def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")      # [text](url) -> text


def normalize(text: str) -> str:
    """Text for comparing versions: ignore link targets (tracking params change on every
    crawl), markdown emphasis and whitespace."""
    text = _LINK_RE.sub(r"\1", text)
    text = re.sub(r"[*_#>`]+", "", text)
    return re.sub(r"\s+", "", text)          # whitespace-insensitive


def section_map(chunks: list[Chunk]) -> dict[str, str]:
    """heading path -> normalized text of that section (chunks joined, in order)."""
    sections: dict[str, list[str]] = {}
    for c in chunks:
        sections.setdefault(" > ".join(c.heading_path), []).append(c.text)
    return {k: normalize(" ".join(v)) for k, v in sections.items()}


_NUM_RE = re.compile(r"(^|> )(?:\d{1,3}(?:\.\d{1,3})*[.)]?\s+)")


def strip_numbers(key: str) -> str:
    """'Guidelines > 2. Safety First' -> 'Guidelines > Safety First' (to spot renumbered clauses)."""
    return _NUM_RE.sub(r"\1", key)


def mark_changes(chunks: list[Chunk], previous: dict[str, str] | None) -> list[str]:
    """Set change_status on each chunk; return headings of sections that were removed.

    first      - no previous version in the index
    unchanged  - same heading, same text
    changed    - same heading (or same title with a new number), different text
    renumbered - same title and text, but the clause number changed
    added      - new section
    """
    current = section_map(chunks)
    if previous is None:
        for c in chunks:
            c.change_status = "first"
        return []

    prev_by_title = {strip_numbers(k): k for k in previous}
    previous_text = "".join(previous.values())
    status, matched = {}, set()
    for key, text in current.items():
        old_key = key if key in previous else prev_by_title.get(strip_numbers(key))
        if old_key is not None:
            matched.add(old_key)
            if previous[old_key] != text:
                status[key] = "changed"
            else:
                status[key] = "unchanged" if old_key == key else "renumbered"
        else:   # new heading - maybe the same text that only got a new heading/format
            status[key] = "unchanged" if text and text in previous_text else "added"
    for c in chunks:
        c.change_status = status[" > ".join(c.heading_path)]

    current_text = "".join(current.values())
    return sorted(k for k in set(previous) - matched if previous[k] not in current_text)


def reuse_llm_fields(out_file: Path, content_hash: str, chunks: list[Chunk]) -> DocumentMetadataLLM | None:
    """If this exact version was already enriched by the LLM, copy the results (no new API calls)."""
    if not out_file.exists():
        return None
    old = json.loads(out_file.read_text(encoding="utf-8"))
    if old["document"]["content_hash"] != content_hash or not old["document"].get("summary"):
        return None
    by_index = {c["chunk_index"]: c for c in old["chunks"]}
    for c in chunks:
        for field in LLM_FIELDS:
            setattr(c, field, by_index.get(c.chunk_index, {}).get(field, getattr(c, field)))
    d = old["document"]
    return DocumentMetadataLLM(title=d["title"], doc_type=d["doc_type"], language=d["language"],
                               summary=d["summary"])


def process_document(
    repo: Path, path: str, versions: list[tuple[Version, str | None]],
    agent: MetadataAgent | None, out_dir: Path,
) -> list[tuple[DocumentMetadata, list[Chunk]]]:
    service, doc_type_name = path.split("/")[0], Path(path).stem
    document_key = f"{slug(service)}/{slug(doc_type_name)}"
    title = f"{service} {doc_type_name}"

    results = []
    previous_sections, previous_doc_id = None, None
    for v, valid_until in versions:
        doc_id = f"{document_key}@{v.date}_{v.commit[:7]}"
        loaded = load_markdown_string(read_text(repo, v, path), source=f"pga-versions/{path}@{v.commit[:7]}")
        chunks = chunk_document(loaded.sections, doc_id)
        removed = mark_changes(chunks, previous_sections)
        out_file = out_dir / document_key / f"{v.date}_{v.commit[:7]}.json"

        llm_meta = reuse_llm_fields(out_file, loaded.content_hash, chunks)
        if llm_meta is None and agent is not None:
            llm_meta = agent.document_metadata(loaded)
            agent.enrich_chunks(chunks, llm_meta)
        if llm_meta is None:   # --no-llm: metadata from the file path only
            llm_meta = DocumentMetadataLLM(title=title, doc_type=DOC_TYPES.get(doc_type_name, "policy"),
                                           language="en", summary="")
        # path-based title/type are exact; the LLM's guesses are not needed for them
        llm_meta = llm_meta.model_copy(update={"title": title,
                                               "doc_type": DOC_TYPES.get(doc_type_name, llm_meta.doc_type)})

        meta = build_document_metadata(loaded, llm_meta, doc_id, len(chunks)).model_copy(update=dict(
            document_key=document_key, service=service, document_type=doc_type_name,
            version_date=v.date, valid_until=valid_until, commit=v.commit,
            is_latest=valid_until is None, previous_doc_id=previous_doc_id, removed_sections=removed,
        ))
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(json.dumps({"document": meta.model_dump(),
                                        "chunks": [c.model_dump() for c in chunks]},
                                       ensure_ascii=False, indent=2), encoding="utf-8")
        results.append((meta, chunks))
        previous_sections, previous_doc_id = section_map(chunks), doc_id
    return results


def main() -> None:
    p = argparse.ArgumentParser(description="Open Terms Archive (pga-versions) -> versioned chunks")
    p.add_argument("repo", help="path to a git clone of OpenTermsArchive/pga-versions")
    p.add_argument("--services", nargs="*", help="e.g. Bluesky Reddit (default: all)")
    p.add_argument("--types", nargs="*", help='e.g. "Terms of Service" "Privacy Policy" (default: all)')
    p.add_argument("--since", help="earliest version date, YYYY-MM-DD")
    p.add_argument("--until", help="latest version date, YYYY-MM-DD")
    p.add_argument("--versions", type=int, default=3, help="newest N distinct versions per document (0 = all)")
    p.add_argument("--out", default="corpus_out")
    p.add_argument("--dry-run", action="store_true", help="only list the versions that would be processed")
    p.add_argument("--no-llm", action="store_true", help="chunks + version metadata only, no API calls")
    p.add_argument("--provider", default="deepseek", choices=list(PROVIDERS))
    p.add_argument("--model", default=None)
    p.add_argument("--concurrency", type=int, default=2)
    p.add_argument("--search", help="BM25 query over the built corpus")
    p.add_argument("--latest-only", action="store_true", help="search only current versions")
    args = p.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    for noisy in ("httpx", "openai", "langchain_openai"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    repo, out_dir = Path(args.repo.strip().strip("\"'")), Path(args.out)
    git(repo, "rev-parse", "HEAD")      # fails early if this is not a git clone
    paths = list_documents(repo, args.services, args.types)
    if not paths:
        raise SystemExit("No documents matched --services/--types")

    plan = []
    for path in paths:
        versions = select_versions(repo, path, args.since, args.until, args.versions or None)
        plan.append((path, versions))
        print(f"{path}: {len(versions)} version(s) " +
              ", ".join(v.date + (" (current)" if until is None else "") for v, until in versions))
    total = sum(len(v) for _, v in plan)
    print(f"\n{len(plan)} documents, {total} versions")
    if args.dry_run:
        return

    agent = None if args.no_llm else MetadataAgent(provider=args.provider, model=args.model,
                                                   max_concurrency=args.concurrency)
    all_docs = []
    manifest = []
    for path, versions in plan:
        if not versions:
            continue
        for meta, chunks in process_document(repo, path, versions, agent, out_dir):
            if meta.previous_doc_id is None:
                print(f"  {meta.doc_id}: {len(chunks)} chunks (first version in the index)")
            else:
                changed = sum(c.change_status in ("added", "changed", "renumbered") for c in chunks)
                print(f"  {meta.doc_id}: {len(chunks)} chunks, {changed} added/changed/renumbered, "
                      f"{len(meta.removed_sections)} sections removed")
            manifest.append({k: getattr(meta, k) for k in (
                "doc_id", "document_key", "service", "document_type", "version_date",
                "valid_until", "is_latest", "num_chunks", "previous_doc_id")})
            all_docs += [c.to_document(meta) for c in chunks]

    # one file with every chunk of every version - what the Retriever indexes
    with open(out_dir / "chunks.jsonl", "w", encoding="utf-8") as f:
        for d in all_docs:
            f.write(json.dumps({"id": d.id, "page_content": d.page_content, "metadata": d.metadata},
                               ensure_ascii=False) + "\n")
    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nSaved {len(all_docs)} chunks to {out_dir / 'chunks.jsonl'} and {out_dir / 'manifest.json'}")

    if args.search:
        from embedding import keyword_search
        docs = [d for d in all_docs if d.metadata["is_latest"]] if args.latest_only else all_docs
        print(f"\nTop matches for: {args.search!r}")
        for rank, d in enumerate(keyword_search(docs, args.search, k=5), 1):
            m = d.metadata
            clause = f"clause {m['clause']} " if m["clause"] else ""
            state = "current" if m["is_latest"] else f"outdated (until {m['valid_until']})"
            print(f"  {rank}. {m['title']} | {clause}{m['clause_title']} | version {m['version_date']} "
                  f"[{state}] | {m['change_status']}")
            print(f"      {m['raw_text'][:160].replace(chr(10), ' ')}...")


if __name__ == "__main__":
    main()
