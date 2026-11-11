# data-agent

Ingestion stage of the ToS Q&A pipeline: **PDF / Markdown → sections → chunks → LLM metadata → JSON / vector store**.
The other agents consume the chunks (`Chunk` / `DocumentMetadata` in `schemas.py`).

| File | Role |
|---|---|
| `file_converter.py` | PDF (via pymupdf4llm) or `.md` → sections with heading path + page |
| `chunker.py` | sections → ~500-token `Chunk`s, `char_start` = offset in `LoadedFile.full_text` |
| `metadata.py` | DeepSeek API: document metadata (1 call) + chunk metadata (1 call per 8 chunks) |
| `embedding.py` | chunks → LangChain `Document`s; BM25 keyword search; optional vector index |
| `pipeline.py` | CLI for single files/folders, writes `output/<name>.<doc_id>.json` |
| `corpus.py` | **versioned corpus** from a git clone of Open Terms Archive `pga-versions` |

## Run

```powershell
$env:DEEPSEEK_API_KEY = "sk-..."
uv sync
uv run python pipeline.py "path\to\terms.pdf"
uv run python pipeline.py ".\docs-folder" --search "How do I get a refund?"
```

Through OrcaRouter instead of the DeepSeek API:

```powershell
$env:ORCAROUTER_API_KEY = "..."
uv run python pipeline.py "path\to\terms.pdf" --provider orcarouter
```

Through OpenRouter with a free NVIDIA model (default `nvidia/nemotron-3-nano-30b-a3b:free`):

```powershell
$env:OPENROUTER_API_KEY = "sk-or-..."
uv run python pipeline.py "path\to\terms.pdf" --provider openrouter
uv run python pipeline.py "path\to\terms.pdf" --provider openrouter --model nvidia/nemotron-nano-9b-v2:free
```

## Versioned corpus (Open Terms Archive)

Versions are git commits, so clone the repository (a ZIP has only the latest version):

```powershell
git clone https://github.com/OpenTermsArchive/pga-versions
uv run python corpus.py pga-versions --services Bluesky Reddit --versions 3 --dry-run
uv run python corpus.py pga-versions --services Bluesky Reddit --versions 3 --no-llm
uv run python corpus.py pga-versions --services Bluesky Reddit --versions 3 --search "minimum age"
```

Output in `corpus_out/`:
- `<service>/<document>/<date>_<commit>.json` - one version: document metadata + chunks
- `chunks.jsonl` - every chunk of every version (`id`, `page_content`, flat `metadata`) for the Retriever
- `manifest.json` - list of versions with `valid_until`, `is_latest`, `previous_doc_id`

Chunk metadata for citations: `document_key`, `version_date`, `valid_until`, `is_latest`,
`clause`, `clause_title`, `heading_path`, `char_start`, `change_status`
(`first` / `unchanged` / `changed` / `renumbered` / `added`).
Re-running reuses saved LLM results for versions that were already processed.
