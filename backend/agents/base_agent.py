from abc import ABC, abstractmethod
from openai import AsyncOpenAI
from config import settings
import json
import re

client = AsyncOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url,
)

class BaseAgent(ABC):
    name: str
    focus_query: str
    system_prompt: str

    def __init__(self, session_id: str):
        self.session_id = session_id

    async def call_llm(self, user_message: str) -> str:
        response = await client.chat.completions.create(
            model=settings.model,
            max_tokens=500,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content

    async def call_llm_json(self, user_message: str) -> dict:
        text = await self.call_llm(
            user_message
            + "\n\nIMPORTANT: Respond ONLY with valid JSON. No markdown fences, no explanation, just raw JSON."
        )
        text = text.strip()
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        return json.loads(text.strip())

    @abstractmethod
    async def run(self, context: str) -> dict:
        pass
