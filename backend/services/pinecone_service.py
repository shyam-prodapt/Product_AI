from pinecone import Pinecone, ServerlessSpec
from config import settings
import asyncio
from typing import List, Dict, Any

class PineconeService:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self._ensure_index()

    def _ensure_index(self):
        existing = [i.name for i in self.pc.list_indexes()]
        if settings.pinecone_index_name not in existing:
            self.pc.create_index(
                name=settings.pinecone_index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )
        self.index = self.pc.Index(settings.pinecone_index_name)

    async def upsert_chunks(self, session_id: str, chunks: List[Dict[str, Any]]):
        vectors = [
            {
                "id": f"{session_id}_{chunk['chunk_id']}",
                "values": chunk["embedding"],
                "metadata": {
                    "session_id": session_id,
                    "text": chunk["text"][:1000],
                    "source": chunk.get("source", "unknown"),
                    "chunk_id": chunk["chunk_id"],
                },
            }
            for chunk in chunks
        ]
        loop = asyncio.get_event_loop()
        for i in range(0, len(vectors), 100):
            batch = vectors[i : i + 100]
            await loop.run_in_executor(None, lambda b=batch: self.index.upsert(vectors=b))

    async def query(self, session_id: str, query_embedding: List[float], top_k: int = 8) -> List[str]:
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(
            None,
            lambda: self.index.query(
                vector=query_embedding,
                top_k=top_k,
                filter={"session_id": {"$eq": session_id}},
                include_metadata=True,
            ),
        )
        return [m.metadata["text"] for m in results.matches]

    async def delete_session(self, session_id: str):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: self.index.delete(filter={"session_id": {"$eq": session_id}}),
        )


_pinecone_service = None

def get_pinecone_service() -> PineconeService:
    global _pinecone_service
    if _pinecone_service is None:
        _pinecone_service = PineconeService()
    return _pinecone_service
