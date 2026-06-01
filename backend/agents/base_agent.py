from abc import ABC, abstractmethod
from openai import AsyncOpenAI
from config import settings
import json
import re

_primary = AsyncOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url,
    timeout=10.0,          # fail fast so Groq fallback kicks in quickly
    max_retries=0,
)

_groq = AsyncOpenAI(
    api_key=settings.groq_api_key or "none",
    base_url=settings.groq_base_url,
) if settings.groq_api_key else None


class BaseAgent(ABC):
    name: str
    focus_query: str
    system_prompt: str

    def __init__(self, session_id: str):
        self.session_id = session_id

    async def call_llm(self, user_message: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message},
        ]
        # Try primary gateway first (hard cap of 500 tokens)
        try:
            resp = await _primary.chat.completions.create(
                model=settings.model,
                max_tokens=500,
                messages=messages,
            )
            return resp.choices[0].message.content
        except Exception:
            pass

        # Fallback to Groq (no gateway cap — use generous limit)
        if _groq is None:
            raise RuntimeError("Primary gateway unreachable and no GROQ_API_KEY configured.")
        resp = await _groq.chat.completions.create(
            model=settings.groq_model,
            max_tokens=1500,
            messages=messages,
        )
        return resp.choices[0].message.content

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
