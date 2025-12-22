import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from agents.base_agent import BaseAgent

class KYCAgent(BaseAgent):

    def evaluate_kyc(self, customer_profile: dict):
        """
        Evaluates KYC / KYB compliance using
        - Bank KYC policies via RAG
        - Customer profile data
        - Strict JSON output for decision automation
        """

        policy_docs = self.retriever.invoke("ABC Bank KYC policy requirements")
        policy_context = "\n\n".join([d.page_content for d in policy_docs])

        prompt = f"""
You are a Senior Banking KYC / KYB Compliance Officer at ABC Bank.

Below is the bank's KYC policy and a customer profile.
You MUST check if the customer satisfies bank compliance standards.

------------------
BANK POLICY DATA
------------------
{policy_context}

------------------
CUSTOMER PROFILE
------------------
{customer_profile}

Rules:
- Do NOT hallucinate
- ONLY use policy + provided data
- If something is missing, mark it missing
- Identify policy compliance & risk
- Explain decisions clearly
- Output must be VALID JSON

Return STRICT VALID JSON ONLY:

{{
 "policy_understanding_summary": "short explanation of what policy expects",
 "kyc_checks_performed": [
   "check 1",
   "check 2"
 ],
 "missing_or_incomplete_requirements": [
   "missing item 1",
   "missing item 2"
 ],
 "compliance_status": "PASS | FAIL | PARTIAL",
 "risk_level": "LOW | MEDIUM | HIGH",
 "justification": "clear business explanation for decision",
 "reference_policy_source": "mention which policy or file section was used"
}}
"""

        return self.run_llm(prompt)
