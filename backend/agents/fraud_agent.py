from agents.base_agent import BaseAgent


class FraudAgent(BaseAgent):

    def __init__(self, retriever):
        super().__init__()
        self.retriever = retriever

    def evaluate_fraud(self, scenario: str):
        """
        Evaluates potential fraud scenarios using bank fraud governance knowledge
        """

        fraud_docs = self.retriever.invoke("ABC Bank fraud risk policies and guidelines")
        policy_context = "\n\n".join([d.page_content for d in fraud_docs])

        prompt = f"""
You are a Senior Banking Fraud Detection & Risk Intelligence Officer at ABC Bank.

Below is the bank's official fraud risk governance knowledge
and details about a customer or transaction scenario.

------------------
BANK FRAUD POLICY
------------------
{policy_context}

------------------
SCENARIO
------------------
{scenario}

Tasks:
- Identify whether behavior is suspicious
- Match possible fraud patterns
- Highlight warning indicators
- Judge fraud risk level
- Be accurate and strict
- NO hallucination
- ONLY use information from policy + implied logic

Return STRICT VALID JSON ONLY:

{{
 "fraud_summary": "short professional explanation",
 "fraud_patterns_detected": [
   "pattern 1",
   "pattern 2"
 ],
 "suspicious_indicators": [
   "indicator 1",
   "indicator 2"
 ],
 "fraud_type_classification": "Identity Fraud | Transaction Fraud | Social Engineering | Account Takeover | Unknown",
 "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
 "recommended_action": "ALLOW | BLOCK | REVIEW_REQUIRED",
 "reference_policy_source": "mention policy source"
}}
"""

        return self.run_llm(prompt)
