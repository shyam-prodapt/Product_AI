import asyncio
import time
from typing import Dict, Any, List
from models.schemas import AgentResult, AgentStatus, AnalysisResponse
from agents.customer_feedback_agent import CustomerFeedbackAgent
from agents.market_research_agent import MarketResearchAgent
from agents.competitor_analysis_agent import CompetitorAnalysisAgent
from agents.feature_prioritization_agent import FeaturePrioritizationAgent
from agents.opportunity_agent import OpportunityAgent
from agents.swot_agent import SwotAgent
from agents.executive_report_agent import ExecutiveReportAgent
from services.pinecone_service import get_pinecone_service
from services.embedding_service import get_embedding


class Orchestrator:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.base_agents = [
            CustomerFeedbackAgent(session_id),
            MarketResearchAgent(session_id),
            CompetitorAnalysisAgent(session_id),
            FeaturePrioritizationAgent(session_id),
            OpportunityAgent(session_id),
        ]

    async def get_context(self, query: str) -> str:
        embedding = await get_embedding(query)
        chunks = await get_pinecone_service().query(self.session_id, embedding, top_k=10)
        return "\n\n---\n\n".join(chunks)

    async def run_agent(self, agent) -> AgentResult:
        start = time.time()
        try:
            context = await self.get_context(agent.focus_query)
            output = await agent.run(context)
            return AgentResult(
                agent_name=agent.name,
                status=AgentStatus.COMPLETED,
                output=output,
                duration_ms=int((time.time() - start) * 1000),
            )
        except Exception as e:
            return AgentResult(
                agent_name=agent.name,
                status=AgentStatus.FAILED,
                error=str(e),
                duration_ms=int((time.time() - start) * 1000),
            )

    async def run_all(self) -> AnalysisResponse:
        # Phase 1: 5 base agents in parallel
        agent_results = await asyncio.gather(*[self.run_agent(a) for a in self.base_agents])

        # Phase 2: Build shared context
        agent_outputs: Dict[str, Any] = {
            r.agent_name: r.output
            for r in agent_results
            if r.status == AgentStatus.COMPLETED
        }

        # Phase 3: SWOT + Executive in parallel (consume base outputs)
        swot_agent = SwotAgent(self.session_id, agent_outputs)
        exec_agent = ExecutiveReportAgent(self.session_id, agent_outputs)

        swot_context, exec_context = await asyncio.gather(
            self.get_context("strengths weaknesses opportunities threats market position"),
            self.get_context("executive summary strategy recommendations roadmap"),
        )

        try:
            swot_result = await swot_agent.run(swot_context)
        except Exception as e:
            swot_result = {"strengths": [], "weaknesses": [], "opportunities": [], "threats": []}
            swot_agent_result_status = AgentStatus.FAILED
            swot_error = str(e)
        else:
            swot_agent_result_status = AgentStatus.COMPLETED
            swot_error = None

        try:
            exec_result = await exec_agent.run(exec_context)
        except Exception as e:
            exec_result = {"executive_summary": "Analysis unavailable — LLM gateway unreachable from this server.", "strategic_recommendations": [], "key_metrics": {}, "action_plan": []}
            exec_agent_result_status = AgentStatus.FAILED
            exec_error = str(e)
        else:
            exec_agent_result_status = AgentStatus.COMPLETED
            exec_error = None

        swot_agent_result = AgentResult(
            agent_name=swot_agent.name,
            status=swot_agent_result_status,
            output=swot_result if isinstance(swot_result, dict) else {},
            error=swot_error,
        )
        exec_agent_result = AgentResult(
            agent_name=exec_agent.name,
            status=exec_agent_result_status,
            output=exec_result if isinstance(exec_result, dict) else {},
            error=exec_error,
        )

        all_results: List[AgentResult] = list(agent_results) + [swot_agent_result, exec_agent_result]

        insights: List[str] = []
        for r in agent_results:
            if r.output and "insights" in r.output:
                insights.extend(r.output["insights"])

        return AnalysisResponse(
            session_id=self.session_id,
            agents=all_results,
            summary=agent_outputs.get("Market Research Agent", {}).get("summary", ""),
            insights=insights[:20],
            opportunities=agent_outputs.get("Opportunity Agent", {}).get("opportunities", []),
            swot=swot_result if isinstance(swot_result, dict) else {},
            feature_priorities=agent_outputs.get("Feature Prioritization Agent", {}).get("features", []),
            roadmap=agent_outputs.get("Feature Prioritization Agent", {}).get("roadmap", []),
            executive_summary=(
                exec_result.get("executive_summary", "")
                if isinstance(exec_result, dict)
                else ""
            ),
        )
