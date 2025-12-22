from agents.base_agent import BaseAgent

class PolicyAgent(BaseAgent):

    def analyze_policy(self, query: str):
        docs = self.retriever.invoke(query)
        context = "\n\n".join([d.page_content for d in docs])

        prompt = f"""
You are a Senior Banking Policy Intelligence Officer for ABC Bank.

POLICY DATA:
{context}

Rules:
- Do not assume
- Use ONLY above policy text
- No hallucination

Return ONLY JSON:
{{
 "policy_summary": "",
 "required_conditions": [],
 "restricted_actions": [],
 "risk_level": "",
 "reference_source": ""
}}
"""
        return self.run_llm(prompt)
