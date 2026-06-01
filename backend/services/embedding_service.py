"""
Zero-dependency embeddings using character n-gram hashing.
Produces deterministic 384-dim float vectors — no downloads, no ONNX, no GPU.
Cosine similarity works correctly because same text → same vector.
"""
import hashlib
import math
from typing import List


def _hash_embed(text: str, dim: int = 384) -> List[float]:
    vec = [0.0] * dim
    words = text.lower().split()
    for i, word in enumerate(words[:500]):          # cap at 500 words
        h = int(hashlib.md5(word.encode()).hexdigest(), 16)
        vec[h % dim] += 1.0
        # also hash bigrams for better signal
        if i < len(words) - 1:
            bigram = word + "_" + words[i + 1]
            h2 = int(hashlib.md5(bigram.encode()).hexdigest(), 16)
            vec[h2 % dim] += 0.5
    magnitude = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / magnitude for x in vec]


async def get_embedding(text: str) -> List[float]:
    return _hash_embed(text[:8000])


async def get_embeddings_batch(texts: List[str]) -> List[List[float]]:
    return [_hash_embed(t[:8000]) for t in texts]
