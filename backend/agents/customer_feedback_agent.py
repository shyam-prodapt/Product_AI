from agents.base_agent import BaseAgent

class CustomerFeedbackAgent(BaseAgent):
    name = "Customer Feedback Agent"
    focus_query = "customer feedback reviews pain points satisfaction complaints feature requests ratings"
    system_prompt = (
        "You are a customer experience analyst. Analyze feedback and sales data. "
        "Respond ONLY with compact valid JSON, no extra text."
    )

    async def run(self, context: str) -> dict:
        prompt = f"""Analyze this data (first 800 chars): {context[:800]}

Return ONLY this JSON (keep all strings under 15 words):
{{"sentiment_score":7.5,"top_pain_points":["point1","point2","point3"],"top_requests":["req1","req2","req3"],"insights":["insight1","insight2","insight3"],"summary":"One sentence summary."}}"""
        return await self.call_llm_json(prompt)
