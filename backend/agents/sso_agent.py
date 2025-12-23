from agents.base_agent import BaseAgent


class SSOAgent(BaseAgent):

    def __init__(self, retriever=None, memory=None):
        super().__init__(retriever)
        self.memory = memory if memory else []

    def evaluate_sso(self, scenario: str):
        """
        Evaluates whether SSO / MFA / secure authentication
        policies must be applied for a given banking scenario.
        """

        policy_docs = self.retriever.invoke("ABC Bank authentication SSO policies")
        policy_context = "\n\n".join([d.page_content for d in policy_docs])

        prompt = f"""
You are a Senior Identity & Access Management Security Officer at ABC Bank.

Below is the bank authentication + SSO governance policy and a user scenario.

-------------------------
BANK SSO / AUTH POLICY
-------------------------
{policy_context}

-------------------------
SCENARIO
-------------------------
{scenario}

You MUST determine:
- Whether SSO is mandatory
- If MFA is required
- Whether request is compliant
- If request should be allowed or denied
- Security risk level
- NO hallucination
- Output STRICT JSON ONLY

Return VALID JSON ONLY:

{{
 "authentication_summary": "short professional explanation",
 "sso_required": "YES | NO",
 "mfa_required": "YES | NO",
 "policy_expectations": [
   "requirement 1",
   "requirement 2"
 ],
 "violations_detected": [
   "violation 1",
   "violation 2"
 ],
 "allowed_or_denied": "ALLOW | DENY | REVIEW_REQUIRED",
 "risk_level": "LOW | MEDIUM | HIGH",
 "reference_source": "SSO / Authentication policy file source"
}}
"""

        return self.run_llm(prompt)
