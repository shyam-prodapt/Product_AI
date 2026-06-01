from typing import List
import asyncio

_model = None

def _get_model():
    global _model
    if _model is None:
        from fastembed import TextEmbedding
        _model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    return _model

async def get_embedding(text: str) -> List[float]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: list(_get_model().embed([text[:8000]]))[0].tolist()
    )

async def get_embeddings_batch(texts: List[str]) -> List[List[float]]:
    loop = asyncio.get_event_loop()
    truncated = [t[:8000] for t in texts]
    def _embed():
        return [emb.tolist() for emb in _get_model().embed(truncated)]
    return await loop.run_in_executor(None, _embed)
