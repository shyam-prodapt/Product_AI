from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse
from services.pinecone_service import get_pinecone_service
from services.embedding_service import get_embedding
from openai import AsyncOpenAI
from config import settings

router = APIRouter()

_primary = AsyncOpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url,
    timeout=10.0,
    max_retries=0,
)

_groq = AsyncOpenAI(
    api_key=settings.groq_api_key or "none",
    base_url=settings.groq_base_url,
) if settings.groq_api_key else None

_SYSTEM = (
    "You are an expert Product Strategy Assistant. Answer questions about the uploaded "
    "business documents. Be precise, data-driven, and actionable. "
    "If the context is insufficient, say so clearly."
)

async def _chat_completion(messages: list) -> str:
    try:
        resp = await _primary.chat.completions.create(
            model=settings.model, max_tokens=500, messages=messages,
        )
        return resp.choices[0].message.content
    except Exception:
        pass
    if _groq is None:
        raise RuntimeError("Primary gateway unreachable and no GROQ_API_KEY configured.")
    resp = await _groq.chat.completions.create(
        model=settings.groq_model, max_tokens=1500, messages=messages,
    )
    return resp.choices[0].message.content


@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    query_embedding = await get_embedding(req.message)
    context_chunks = await get_pinecone_service().query(req.session_id, query_embedding, top_k=6)
    context = "\n\n---\n\n".join(context_chunks)
    messages = [{"role": "system", "content": _SYSTEM}]
    messages.extend(req.history or [])
    messages.append({
        "role": "user",
        "content": (
            f"Context from uploaded documents:\n{context}\n\n"
            f"User question: {req.message}\n\n"
            "Answer based on the context provided. Be specific and cite data points."
        ),
    })
    answer = await _chat_completion(messages)
    return ChatResponse(
        response=answer,
        sources=[f"Source chunk {i + 1}" for i in range(min(3, len(context_chunks)))],
    )
