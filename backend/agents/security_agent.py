import os
from agents.base_agent import BaseAgent


class SecurityAgent(BaseAgent):

    def __init__(self, retriever):
        super().__init__()
        self.retriever = retriever


    def evaluate_security(self, query: str):
        """
        Evaluates security & privacy compliance rules using bank governance data
        """

        docs = self.retriever.invoke(query)
        context = "\n\n".join([d.page_content for d in docs])

        prompt = f"""
You are a Senior Banking Security & Privacy Compliance Officer.
You work for ABC Bank and must strictly follow banking governance, security,
data protection, and privacy regulations.

SECURITY DATA:
{context}

TASK:
Analyze the security and privacy expectations related to the user request below.
Identify whether actions comply with:
- Data Protection
- Role based Access
- Sensitive information handling
- Storage & Retention
- Encryption and masking needs
- Fraud or misuse prevention policies

USER REQUEST / SCENARIO:
{query}

RULES:
- Do NOT hallucinate
- Use only given policy knowledge
- If information is missing, mention explicitly
- Be strict and professional

Return STRICT VALID JSON:

{{
 "security_summary": "short professional explanation",
 "sensitive_data_detected": [
     "data type 1",
     "data type 2"
 ],
 "required_security_controls": [
     "control requirement 1",
     "control requirement 2"
 ],
 "violations_detected": [
     "violation 1",
     "violation 2"
 ],
 "allowed_or_denied": "ALLOW | DENY | REVIEW_REQUIRED",
 "risk_level": "LOW | MEDIUM | HIGH",
 "reference_source": "which policy file supported the decision"
}}
"""

        return self.run_llm(prompt)
        
