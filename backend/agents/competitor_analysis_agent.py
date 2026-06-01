from agents.base_agent import BaseAgent

class CompetitorAnalysisAgent(BaseAgent):
    name = "Competitor Analysis Agent"
    focus_query = "competitors competitive landscape product comparison market position pricing category performance"
    system_prompt = (
        "You are a competitive intelligence analyst. Analyze product and category performance. "
        "Respond ONLY with compact valid JSON, no extra text."
    )

    async def run(self, context: str) -> dict:
        prompt = f"""Analyze competitive landscape (first 800 chars): {context[:800]}

Return ONLY this JSON (keep all strings under 12 words):
{{"competitors":[{{"name":"name","strengths":["s1"],"weaknesses":["w1"],"market_position":"position"}},{{"name":"name2","strengths":["s1"],"weaknesses":["w1"],"market_position":"position"}}],"competitive_gaps":["gap1","gap2"],"top_performing_categories":["cat1","cat2"],"insights":["insight1","insight2"],"summary":"One sentence."}}"""
        return await self.call_llm_json(prompt)
