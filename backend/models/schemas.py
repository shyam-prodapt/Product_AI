from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum

class AgentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class AgentResult(BaseModel):
    agent_name: str
    status: AgentStatus
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    duration_ms: Optional[int] = None

class AnalysisRequest(BaseModel):
    session_id: str
    focus_areas: Optional[List[str]] = None

class AnalysisResponse(BaseModel):
    session_id: str
    agents: List[AgentResult]
    summary: str
    insights: List[str]
    opportunities: List[Dict[str, Any]]
    swot: Dict[str, List[str]]
    feature_priorities: List[Dict[str, Any]]
    roadmap: List[Dict[str, Any]]
    executive_summary: str

class ChatRequest(BaseModel):
    session_id: str
    message: str
    history: Optional[List[Dict[str, str]]] = []

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = []

class UploadResponse(BaseModel):
    session_id: str
    files_processed: int
    chunks_indexed: int
    message: str
