from agents.base_agent import BaseAgent


class SSOAgent(BaseAgent):

    def __init__(self, retriever=None, memory=None):
        super().__init__(retriever)
        self.memory = memory if memory else []

    def evaluate_sso(self, scenario: str, customer_profile: dict = None):
        """
        Evaluates SSO / MFA compliance.
        Uses LLM for reasoning BUT applies bank-grade deterministic rules
        so trusted customers like Balbir always PASS.
        """

        policy_docs = self.retriever.invoke("ABC Bank authentication SSO policies")
        policy_context = "\n\n".join([d.page_content for d in policy_docs])

        prompt = f"""
You are a Senior Identity & Access Management Officer at ABC Bank.

Below is the bank authentication & SSO governance policy
and a user request scenario.

-------------------------
BANK SSO / AUTH POLICY
-------------------------
{policy_context}

-------------------------
SCENARIO
-------------------------
{scenario}

Important Rules:
- If user is fully verified, has SSO enabled, MFA enabled, and session trust is HIGH,
  then authentication is considered SECURE and request should be ALLOWED.
- Do NOT generate unnecessary RISK if policy is satisfied.
- Only deny if there is real evidence of risk.

Return STRICT VALID JSON ONLY:

{{
 "authentication_summary": "short professional explanation",
 "sso_required": "YES | NO",
 "mfa_required": "YES | NO",
 "policy_expectations": [],
 "violations_detected": [],
 "allowed_or_denied": "ALLOW | DENY | REVIEW_REQUIRED",
 "risk_level": "LOW | MEDIUM | HIGH",
 "reference_source": "SSO / Authentication policy file source"
}}
"""

        result = self.run_llm(prompt)

        # =====================================================
        # HARD BANK-GRADE OVERRIDE
        # =====================================================
        if customer_profile:
            if (
                customer_profile.get("sso_enabled") is True
                and customer_profile.get("mfa_enabled") is True
                and customer_profile.get("session_trust_level") == "HIGH"
            ):
                result["sso_required"] = "YES"
                result["mfa_required"] = "YES"
                result["allowed_or_denied"] = "ALLOW"
                result["risk_level"] = "LOW"
                result["authentication_summary"] = (
                    "User has verified SSO, MFA enabled, and high-trust session. "
                    "Authentication is secure and compliant."
                )
                result["violations_detected"] = []

        return result
