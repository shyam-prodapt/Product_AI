from fastapi import APIRouter, HTTPException
from models.schemas import AnalysisRequest, AnalysisResponse
from agents.orchestrator import Orchestrator
import traceback

router = APIRouter()

@router.post("/run", response_model=AnalysisResponse)
async def run_analysis(req: AnalysisRequest):
    try:
        orchestrator = Orchestrator(session_id=req.session_id)
        return await orchestrator.run_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}\n{traceback.format_exc()}")
