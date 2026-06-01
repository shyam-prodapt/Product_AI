from openai import AsyncOpenAI
from config import settings
from typing import List
import asyncio

client = AsyncOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url,
)

async def get_embedding(text: str) -> List[float]:
    response = await client.embeddings.create(
        input=text[:8000],
        model=settings.embedding_model,
    )
    return response.data[0].embedding

async def get_embeddings_batch(texts: List[str]) -> List[List[float]]:
    tasks = [get_embedding(t) for t in texts]
    return await asyncio.gather(*tasks)
