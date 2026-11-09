import requests
import json
import urllib3
import time
import re
import os
from collections import deque
from dotenv import load_dotenv

load_dotenv("data_for_API.env")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "sub_queries": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "id":         {"type": "string"},
                    "text":       {"type": "string"},
                    "type":       {"type": "string", "enum": ["lookup", "synthesis"]},
                    "depends_on": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["id", "text", "type", "depends_on"],
                "additionalProperties": False
            }
        }
    },
    "required": ["sub_queries"],
    "additionalProperties": False
}


class PlannerAgent:
    def __init__(self, model='GigaChat'):
        self.model = model
        self.rquid = os.getenv("GIGACHAT_RQUID")
        self.basic_auth = os.getenv("BASIC_AUTH")
        self.oauth_url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        self.api_url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

        self.access_token = None
        self.token_expires_at = 0

        self.system_prompt = """Ты — агент-планировщик в системе Compliance RAG.
        Твоя задача — разбить вопрос пользователя на исполнимый план поиска.

        ПРАВИЛА:
        1. Каждый шаг — объект: "id", "text", "type" ("lookup" или "synthesis"), "depends_on".
        2. "lookup" ищет факты в документах. "synthesis" сравнивает или обобщает результаты других шагов.
        3. "synthesis" ВСЕГДА должен иметь непустой "depends_on" (список id шагов).
        4. Если вопрос требует сравнения, поиска в разных версиях или документах — ОБЯЗАТЕЛЬНО делай декомпозицию.
        5. Если вопрос простой (один факт) — верни один lookup.
        6. Никаких циклов.

        КОНТЕКСТ ДИАЛОГА (ВАЖНО):
        Тебе может быть передана история предыдущих сообщений. 
        Если текущий вопрос пользователя неполный (например, "А в 2023 году?", "А что насчет возврата?"), ОБЯЗАТЕЛЬНО восстанови полный смысл, используя историю. 
        В поле "text" для поиска всегда пиши самодостаточные, полные фразы, а не просто "А в 2023?".

        ПРИМЕРЫ:
        Вопрос: "Какие правила конфиденциальности действовали в 2022 году и как они изменились в 2023?"
        Ответ:
        {
          "sub_queries": [
            {"id": "q1", "text": "правила конфиденциальности версия 2022", "type": "lookup", "depends_on": []},
            {"id": "q2", "text": "правила конфиденциальности версия 2023", "type": "lookup", "depends_on": []},
            {"id": "q3", "text": "Как изменились правила конфиденциальности с 2022 по 2023 год?", "type": "synthesis", "depends_on": ["q1", "q2"]}
          ]
        }

        Ответ — строго валидный JSON-объект вида {"sub_queries": [...]}. Без пояснений."""



    def get_token(self):
        if self.access_token and time.time() < (self.token_expires_at - 60):
            return self.access_token

        print("Обновление токена...")
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': self.rquid,
            'Authorization': f'Basic {self.basic_auth}'
        }
        payload = {'scope': 'GIGACHAT_API_PERS'}

        response = requests.post(self.oauth_url, headers=headers, data=payload, verify=False)

        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']

            expires_at_ms = data.get('expires_at')
            if expires_at_ms:
                self.token_expires_at = expires_at_ms / 1000.0
            else:
                self.token_expires_at = time.time() + 1800

            return self.access_token
        else:
            raise RuntimeError(f"Ошибка получения токена: {response.status_code} - {response.text}")



    def _invoke_API(self, messages, response_format=None, retry=True):
        token = self.get_token()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        body = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "repetition_penalty": 1.0
        }
        if response_format is not None:
            body["response_format"] = response_format

        response = requests.post(
            self.api_url, headers=headers,
            data=json.dumps(body), verify=False
        )

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        elif response.status_code == 401 and retry:
            print("Токен протух, пробуем обновить...")
            self.access_token = None
            return self._invoke_API(messages, response_format, retry=False)
        else:
            raise RuntimeError(f"Ошибка API ({response.status_code}): {response.text}")



    def _validate_plan(self, raw_plan):
        """Возвращает (ok, error_message)."""
        if not isinstance(raw_plan, dict) or "sub_queries" not in raw_plan:
            return False, "нет поля sub_queries"
        nodes = raw_plan["sub_queries"]
        if not isinstance(nodes, list) or len(nodes) == 0:
            return False, "sub_queries пуст или не массив"

        ids = set()
        for n in nodes:
            if not isinstance(n, dict):
                return False, "узел плана — не объект"
            for f in ("id", "text", "type", "depends_on"):
                if f not in n:
                    return False, f"у узла отсутствует поле {f}"
            if n["type"] not in ("lookup", "synthesis"):
                return False, f"недопустимый type: {n['type']}"
            if not isinstance(n["depends_on"], list):
                return False, "depends_on — не массив"
            if n["id"] in ids:
                return False, f"дубликат id: {n['id']}"
            ids.add(n["id"])
            if not isinstance(n["text"], str) or not n["text"].strip():
                return False, f"пустой text у узла {n['id']}"

        for n in nodes:
            for dep in n["depends_on"]:
                if dep not in ids:
                    return False, f"узел {n['id']} зависит от несуществующего {dep}"
            if n["type"] == "synthesis" and not n["depends_on"]:
                return False, f"synthesis-узел {n['id']} без depends_on"

        return True, None



    def _topo_levels(self, nodes):
        """Возвращает список уровней [[node, ...], ...]
        или None, если в графе есть цикл."""
        indeg = {n["id"]: len(n["depends_on"]) for n in nodes}
        children = {n["id"]: [] for n in nodes}
        by_id = {n["id"]: n for n in nodes}
        for n in nodes:
            for dep in n["depends_on"]:
                children[dep].append(n["id"])

        level = [nid for nid, d in indeg.items() if d == 0]
        levels = []
        visited = 0
        while level:
            levels.append([by_id[nid] for nid in level])
            visited += len(level)
            next_level = []
            for nid in level:
                for child in children[nid]:
                    indeg[child] -= 1
                    if indeg[child] == 0:
                        next_level.append(child)
            level = next_level

        if visited != len(nodes):
            return None  # цикл
        return levels

    def _topo_sort(self, nodes):
        """Плоский порядок. Нужен, если оркестратор последовательный."""
        levels = self._topo_levels(nodes)
        if levels is None:
            return None
        return [n for lvl in levels for n in lvl]



    def _fallback_plan(self, user_question):
        return [{"id": "q1", "text": user_question, "type": "lookup", "depends_on": []}]



    def plan(self, user_question, history=None):
        messages = [{"role": "system", "content": self.system_prompt}]
        if history:
            truncated_history = history[-10:]
            messages.extend(truncated_history)
        messages.append({"role": "user", "content": user_question})

        raw = None
        try:
            raw = self._invoke_API(
                messages,
                response_format={
                    "type": "json_schema",
                    "json_schema": {"name": "Plan", "strict": True, "schema": PLAN_SCHEMA}
                }
            )
        except RuntimeError as e:

            print(f"[Planner] strict-схема не сработала ({e}), пробуем json_object")
            try:
                raw = self._invoke_API(messages, response_format={"type": "json_object"})
            except RuntimeError as e2:
                print(f"[Planner] json_object тоже не сработал: {e2}")
                return self._fallback_plan(user_question)


        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            m = re.search(r'\{.*\}', raw, re.DOTALL)
            if not m:
                print(f"[Planner] не нашли JSON в ответе: {raw[:200]}")
                return self._fallback_plan(user_question)
            try:
                parsed = json.loads(m.group(0))
            except json.JSONDecodeError as e:
                print(f"[Planner] JSON невалиден: {e}")
                return self._fallback_plan(user_question)


        ok, err = self._validate_plan(parsed)
        if not ok:
            print(f"[Planner] валидация плана провалена: {err}")
            return self._fallback_plan(user_question)


        nodes = parsed["sub_queries"]
        ordered = self._topo_sort(nodes)
        if ordered is None:
            print("[Planner] в плане обнаружен цикл — откат")
            return self._fallback_plan(user_question)

        return ordered


