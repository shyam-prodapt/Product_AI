from agents.base_agent import BaseAgent

class FeaturePrioritizationAgent(BaseAgent):
    name = "Feature Prioritization Agent"
    focus_query = "features product improvements user stories backlog priority impact effort roadmap"
    system_prompt = (
        "You are a product manager specializing in feature prioritization. "
        "Respond ONLY with compact valid JSON, no extra text."
    )

    async def run(self, context: str) -> dict:
        prompt = f"""Prioritize features from this data (first 800 chars): {context[:800]}

Return ONLY this JSON (strings under 10 words, priority_score = impact/effort as float):
{{"features":[{{"name":"Feature A","impact":9,"effort":3,"priority_score":3.0,"rationale":"reason"}},{{"name":"Feature B","impact":8,"effort":4,"priority_score":2.0,"rationale":"reason"}},{{"name":"Feature C","impact":7,"effort":5,"priority_score":1.4,"rationale":"reason"}},{{"name":"Feature D","impact":6,"effort":4,"priority_score":1.5,"rationale":"reason"}}],"roadmap":[{{"quarter":"Q3 2026","features":["Feature A","Feature B"],"theme":"theme1"}},{{"quarter":"Q4 2026","features":["Feature C","Feature D"],"theme":"theme2"}}],"insights":["insight1","insight2"]}}"""
        return await self.call_llm_json(prompt)
