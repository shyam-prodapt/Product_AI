from agents.base_agent import BaseAgent

class MarketResearchAgent(BaseAgent):
    name = "Market Research Agent"
    focus_query = "market trends industry analysis market size growth rate target segments regional performance"
    system_prompt = (
        "You are a market analyst. Identify trends and opportunities from sales data. "
        "Respond ONLY with compact valid JSON, no extra text."
    )

    async def run(self, context: str) -> dict:
        prompt = f"""Analyze this market data (first 800 chars): {context[:800]}

Return ONLY this JSON (keep all strings under 15 words):
{{"market_trends":["trend1","trend2","trend3"],"target_segments":[{{"segment":"name","opportunity":"description"}}],"growth_opportunities":["opp1","opp2","opp3"],"insights":["insight1","insight2","insight3"],"summary":"One sentence overview."}}"""
        return await self.call_llm_json(prompt)
