from agents.base_agent import BaseAgent

class OpportunityAgent(BaseAgent):
    name = "Opportunity Agent"
    focus_query = "business opportunities product gaps growth areas innovation untapped markets high margin"
    system_prompt = (
        "You are an opportunity analyst. Find high-value product and business opportunities. "
        "Respond ONLY with compact valid JSON, no extra text."
    )

    async def run(self, context: str) -> dict:
        prompt = f"""Find opportunities in this data (first 800 chars): {context[:800]}

Return ONLY this JSON (strings under 15 words):
{{"opportunities":[{{"title":"Opp Title","description":"Brief description under 15 words.","score":9,"category":"Growth","rationale":"reason"}},{{"title":"Opp Title 2","description":"Brief description.","score":8,"category":"Innovation","rationale":"reason"}},{{"title":"Opp Title 3","description":"Brief description.","score":7,"category":"Product","rationale":"reason"}}],"insights":["insight1","insight2","insight3"]}}"""
        return await self.call_llm_json(prompt)
