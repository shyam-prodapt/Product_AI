from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse
from services.pinecone_service import get_pinecone_service
from services.embedding_service import get_embedding
from openai import AsyncOpenAI
from config import settings

router = APIRouter()
client = AsyncOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url,
)

@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    query_embedding = await get_embedding(req.message)
    context_chunks = await get_pinecone_service().query(req.session_id, query_embedding, top_k=6)
    context = "\n\n---\n\n".join(context_chunks)
    messages = list(req.history or [])
    messages.append(
        {
            "role": "user",
            "content": (
                f"Context from uploaded documents:\n{context}\n\n"
                f"User question: {req.message}\n\n"
                "Answer based on the context provided. Be specific and cite data points."
            ),
        }
    )
    response = await client.chat.completions.create(
        model=settings.model,
        max_tokens=500,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert Product Strategy Assistant. Answer questions about the uploaded "
                    "business documents. Be precise, data-driven, and actionable. "
                    "If the context is insufficient, say so clearly."
                ),
            }
        ]
        + messages,
    )
    return ChatResponse(
        response=response.choices[0].message.content,
        sources=[f"Source chunk {i + 1}" for i in range(min(3, len(context_chunks)))],
    )
