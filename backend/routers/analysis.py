from fastapi import APIRouter
from models.schemas import AnalysisRequest, AnalysisResponse
from agents.orchestrator import Orchestrator

router = APIRouter()

@router.post("/run", response_model=AnalysisResponse)
async def run_analysis(req: AnalysisRequest):
    orchestrator = Orchestrator(session_id=req.session_id)
    return await orchestrator.run_all()
