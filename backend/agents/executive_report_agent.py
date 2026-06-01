from agents.base_agent import BaseAgent
from typing import Dict, Any
import json

class ExecutiveReportAgent(BaseAgent):
    name = "Executive Report Agent"
    focus_query = "executive summary strategy recommendations roadmap key metrics action plan"
    system_prompt = (
        "You are a C-suite strategist. Write a concise executive summary with recommendations. "
        "Respond ONLY with compact valid JSON, no extra text."
    )

    def __init__(self, session_id: str, agent_outputs: Dict[str, Any]):
        super().__init__(session_id)
        self.agent_outputs = agent_outputs

    async def run(self, context: str) -> dict:
        # Compact serialization to stay within token budget
        summary = json.dumps(self.agent_outputs, indent=None, separators=(',', ':'))[:1200]
        prompt = f"""Write executive report. Data: {summary}

Return ONLY this JSON (executive_summary max 2 sentences, recommendations max 10 words each):
{{"executive_summary":"Two sentence summary of strategy and key finding.","strategic_recommendations":["rec1","rec2","rec3"],"key_metrics":{{"top_revenue_driver":"product name","highest_growth_region":"region","customer_satisfaction":"score","primary_risk":"risk"}}}}"""
        return await self.call_llm_json(prompt)
