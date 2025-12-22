from agents.base_agent import BaseAgent


class SecurityAgent(BaseAgent):

    def analyze_security(self, query: str, policy_context: str):
        prompt = f"""
You are ABC Bank Senior Security & Privacy Compliance Officer.

Using ONLY the below official bank security policy, evaluate the query.

SECURITY POLICY:
{policy_context}

USER QUERY:
{query}

Rules:
- Do NOT hallucinate
- Only use information in policy context
- Be strict
- Return ONLY JSON. No extra text.

Return JSON in this format:

{{
 "security_summary": "",
 "sensitive_data_detected": [],
 "required_security_controls": [],
 "violations_detected": [],
 "allowed_or_denied": "ALLOW | DENY | REVIEW_REQUIRED",
 "risk_level": "LOW | MEDIUM | HIGH",
 "reference_source": "ABC BANK SECURITY & PRIVACY RULES"
}}
"""

        return self.run_llm(prompt)
