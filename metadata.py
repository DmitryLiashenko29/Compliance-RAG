from __future__ import annotations

import logging
import os
import re

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda
from pydantic import BaseModel

from schemas import Chunk, ChunkBatchLLM, DocumentMetadata, DocumentMetadataLLM, LoadedFile

log = logging.getLogger(__name__)

# provider -> (base_url, API-key env var, default model).
# All are OpenAI-compatible, so the same client works for each.
PROVIDERS = {
    "deepseek":   ("https://api.deepseek.com",     "DEEPSEEK_API_KEY",   "deepseek-chat"),
    "orcarouter": ("https://api.orcarouter.ai/v1", "ORCAROUTER_API_KEY", "deepseek/deepseek-chat"),
    # free NVIDIA model; other ids: openrouter.ai/models?q=nvidia
    "openrouter": ("https://openrouter.ai/api/v1",  "OPENROUTER_API_KEY", "nvidia/nemotron-3.5-lightning:free"),
}
DEFAULT_PROVIDER = "deepseek"
CHUNKS_PER_CALL = 8          # chunks annotated in one LLM call
MAX_DOC_CHARS = 200_000      # text sent for document-level metadata (~50k tokens, model has 128k)


DOC_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You extract accurate, concise metadata from documents for a search index. "
               "Use only information present in the document."),
    ("human", "<document source='{source}'>\n{text}\n</document>\n\nExtract document metadata."),
])

CHUNK_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You annotate document chunks for retrieval. Be specific and factual."),
    ("human", "Document title: {title}\nDocument summary: {summary}\n\n{chunks}\n\n"
              "Return metadata for every chunk above, keeping the same chunk_index."),
])


def make_llm(provider: str = DEFAULT_PROVIDER, model: str | None = None):
    from langchain_openai import ChatOpenAI   # all providers speak the OpenAI API

    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider {provider!r}; choose from {list(PROVIDERS)}")
    base_url, key_env, default_model = PROVIDERS[provider]
    api_key = os.environ.get(key_env)
    if not api_key:
        raise RuntimeError(f"Set the {key_env} environment variable to use {provider}")
    model = model or default_model
    # reasoning models (deepseek-reasoner / r1) reject the temperature parameter
    extra = {} if ("reasoner" in model or "r1" in model) else {"temperature": 0}
    return ChatOpenAI(model=model, api_key=api_key, timeout=120,
                      base_url=os.environ.get(f"{provider.upper()}_BASE_URL", base_url), **extra)


# How each provider returns structured data:
#  "tools" - forced tool calling (reliable, but needs tool_choice support from the host)
#  "json"  - JSON schema in the prompt + parsing (works on any model, incl. free OpenRouter ones)
STRUCTURED_MODE = {"deepseek": "tools", "orcarouter": "tools", "openrouter": "json"}

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)


def structured(llm, schema: type[BaseModel], mode: str) -> Runnable:
    if mode == "tools":
        return llm.with_structured_output(schema, method="function_calling")

    parser = PydanticOutputParser(pydantic_object=schema)
    instructions = HumanMessage(
        parser.get_format_instructions()
        + "\nReply with the JSON object only - no explanations, no markdown."
    )

    def add_instructions(prompt_value):
        return prompt_value.to_messages() + [instructions]

    def strip_reasoning(msg: AIMessage) -> str:
        # some reasoning models put <think>...</think> before the answer
        return _THINK_RE.sub("", msg.content if isinstance(msg.content, str) else str(msg.content))

    return RunnableLambda(add_instructions) | llm | RunnableLambda(strip_reasoning) | parser


class MetadataAgent:
    def __init__(
        self,
        provider: str = DEFAULT_PROVIDER,
        model: str | None = None,
        max_concurrency: int = 2,
        batch_size: int = CHUNKS_PER_CALL,
        max_doc_chars: int = MAX_DOC_CHARS,
    ):
        self.batch_size = batch_size
        self.max_doc_chars = max_doc_chars
        self.max_concurrency = max_concurrency
        llm = make_llm(provider, model)
        mode = STRUCTURED_MODE[provider]
        retry = dict(stop_after_attempt=3, wait_exponential_jitter=True)
        self.doc_chain = (DOC_PROMPT | structured(llm, DocumentMetadataLLM, mode)).with_retry(**retry)
        self.chunk_chain = (CHUNK_PROMPT | structured(llm, ChunkBatchLLM, mode)).with_retry(**retry)

    def document_metadata(self, doc: LoadedFile) -> DocumentMetadataLLM:
        return self.doc_chain.invoke({"source": doc.source, "text": doc.full_text[: self.max_doc_chars]})

    def enrich_chunks(self, chunks: list[Chunk], doc_meta: DocumentMetadataLLM) -> list[Chunk]:
        by_index = {c.chunk_index: c for c in chunks}
        inputs = []
        for start in range(0, len(chunks), self.batch_size):
            batch = chunks[start:start + self.batch_size]
            inputs.append({
                "title": doc_meta.title,
                "summary": doc_meta.summary,
                "chunks": "\n\n".join(
                    f"<chunk index='{c.chunk_index}' section='{' > '.join(c.heading_path)}'>\n"
                    f"{c.text}\n</chunk>"
                    for c in batch
                ),
            })

        results = self.chunk_chain.batch(
            inputs, config={"max_concurrency": self.max_concurrency}, return_exceptions=True
        )
        for n, result in enumerate(results):
            if isinstance(result, Exception):
                log.error("Chunk batch %d not enriched: %s", n, result)
                continue
            for m in result.chunks:
                c = by_index.get(m.chunk_index)
                if c is None:
                    continue
                c.summary, c.keywords, c.questions = m.summary, m.keywords, m.questions
                c.content_type, c.context = m.content_type, m.context
        return chunks


def build_document_metadata(
    doc: LoadedFile, llm_meta: DocumentMetadataLLM, doc_id: str, num_chunks: int
) -> DocumentMetadata:
    return DocumentMetadata(
        **llm_meta.model_dump(),
        doc_id=doc_id,
        source=doc.source,
        file_type=doc.file_type,
        content_hash=doc.content_hash,
        num_chunks=num_chunks,
    )
