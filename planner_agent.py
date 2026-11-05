import requests
import json
import urllib3
import time
from dotenv import load_dotenv
import os
import re

load_dotenv("data_for_API.env")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
Твоя задача — разбить сложный вопрос пользователя по нормативным документам на простые подзапросы для поиска.
Если вопрос уже простой, верни его без изменений (массив из одного элемента).
Ответь СТРОГО в формате JSON-массива строк. Не пиши никаких вступительных слов, только чистый JSON.
Пример ответа: ["правила конфиденциальности версия 2022", "правила конфиденциальности версия 2023"]"""

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
        # ИСПРАВЛЕНО: 'scope' вместо 'score'
        payload = {'scope': 'GIGACHAT_API_PERS'}

        response = requests.post(self.oauth_url, headers=headers, data=payload, verify=False)

        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']

            # ИСПРАВЛЕНО: GigaChat отдает expires_at в миллисекундах (Unix timestamp)
            expires_at_ms = data.get('expires_at')
            if expires_at_ms:
                self.token_expires_at = expires_at_ms / 1000.0
            else:
                self.token_expires_at = time.time() + 1800  # Фолбэк: 30 минут

            return self.access_token
        else:
            raise RuntimeError(f"Ошибка получения токена: {response.status_code} - {response.text}")

    def _invoke_API(self, messages, retry=True):
        token = self.get_token()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        payload = json.dumps({
            "model": self.model,
            "messages": messages,
            "stream": False,
            "repetition_penalty": 1
        })

        response = requests.post(self.api_url, headers=headers, data=payload, verify=False)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        elif response.status_code == 401 and retry:
            print("Токен протух, пробуем обновить...")
            self.access_token = None
            return self._invoke_API(messages, retry=False)
        else:
            raise RuntimeError(f"Ошибка API ({response.status_code}): {response.text}")

    def plan(self, user_question):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_question}
        ]

        raw_content = self._invoke_API(messages)

        try:
            match = re.search(r'\[.*\]', raw_content, re.DOTALL)
            if not match:
                raise ValueError("В ответе LLM не найден JSON-массив")

            clean_json = match.group(0)
            sub_queries = json.loads(clean_json)

            # ИСПРАВЛЕНО: проверяем, что это массив СТРОК (а не словарей)
            if not isinstance(sub_queries, list) or not all(isinstance(item, str) for item in sub_queries):
                raise ValueError("JSON не является массивом строк")

            return sub_queries
        except (json.JSONDecodeError, ValueError) as e:
            print(f'Ошибка парсинга ответа LLM: {e}')
            print(f'Сырой ответ: {raw_content}')
            return [user_question]




