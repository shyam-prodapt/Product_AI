from agents.base_agent import BaseAgent
from typing import Dict, Any
import json

class SwotAgent(BaseAgent):
    name = "SWOT Analysis Agent"
    focus_query = "strengths weaknesses opportunities threats market position competitive advantage"
    system_prompt = (
        "You are a strategic consultant. Synthesize data into a SWOT analysis. "
        "Respond ONLY with compact valid JSON, no extra text."
    )

    def __init__(self, session_id: str, agent_outputs: Dict[str, Any]):
        super().__init__(session_id)
        self.agent_outputs = agent_outputs

    async def run(self, context: str) -> dict:
        # Keep summary small to fit within 500 token response limit
        summary = json.dumps(self.agent_outputs, indent=None, separators=(',', ':'))[:1000]
        prompt = f"""Synthesize into SWOT. Data: {summary} Context: {context[:400]}

Return ONLY this JSON (3-4 items per list, strings under 12 words):
{{"strengths":["s1","s2","s3"],"weaknesses":["w1","w2","w3"],"opportunities":["o1","o2","o3"],"threats":["t1","t2","t3"]}}"""
        return await self.call_llm_json(prompt)
