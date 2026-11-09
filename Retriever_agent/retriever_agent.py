"""Агент Поиска (Retriever) для Compliance RAG.

Вход:  подзапросы от Planner (или дополнительный запрос от Критика).
Выход: найденные фрагменты с документом, версией, пунктом и оценкой сходства.

Retriever всегда возвращает k фрагментов, даже если ответа в корпусе нет,
а оценка сходства - не вероятность правильного ответа. Поэтому решение
"хватает ли найденного" принимает Критик, а не этот агент.
"""
import os

import openai
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

# ---------- Настройки ----------
API_KEY = os.environ["OPENROUTER_API_KEY"]
BASE_URL = os.getenv("BASE_URL", "https://openrouter.ai/api/v1")
CHAT_MODEL = os.getenv("CHAT_MODEL", "openai/gpt-4o-mini")
EMBED_MODEL = os.getenv("EMBED_MODEL", "qwen/qwen3-embedding-0.6b")

# Поля metadata, которые проставляет Агент Документов.
# version - дата в формате ГГГГ-ММ-ДД (так версии сравниваются как строки).
DOC_KEY, VERSION_KEY, CLAUSE_KEY = "document", "version", "clause"

embeddings = OpenAIEmbeddings(
    model=EMBED_MODEL,
    base_url=BASE_URL,
    api_key=API_KEY,
    check_embedding_ctx_length=False,
    request_timeout=20,
    max_retries=1,
)
llm = ChatOpenAI(
    model=CHAT_MODEL,
    base_url=BASE_URL,
    api_key=API_KEY,
    temperature=0,
    timeout=20,
    max_retries=1,
)
