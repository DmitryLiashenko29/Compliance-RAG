"""Подбор порога MIN_SCORE: сравниваем сходство для вопросов с ответом и без ответа.

Заполните два списка вопросами из эталона (30-50 вопросов) и запустите скрипт.
Порог - где-то между самым низким баллом "есть ответ" и самым высоким "нет ответа".
"""
from retriever_agent import RetrieverAgent, demo_chunks

with_answer = ["Сколько дней хранятся логи сейчас?"]   # TODO: вопросы из эталона, где ответ есть
without_answer = ["Какая сегодня погода в Москве?"]    # TODO: вопросы из эталона без ответа

agent = RetrieverAgent(demo_chunks())  # TODO: заменить на чанки Агента Документов


def best_score(question):
    hits = agent.search(question, k=1, mode="all", min_score=-1)
    return hits[0]["score"] if hits else None


print("Есть ответ:  ", [(q, best_score(q)) for q in with_answer])
print("Нет ответа:  ", [(q, best_score(q)) for q in without_answer])
