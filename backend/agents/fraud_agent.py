from agents.base_agent import BaseAgent


class FraudAgent(BaseAgent):

    def __init__(self, retriever=None, memory=None):
        super().__init__(retriever)
        self.memory = memory if memory else []

    def evaluate_fraud(self, scenario: str, customer_profile: dict = None):
        """
        Hybrid Fraud Analysis:
          Uses LLM reasoning on fraud policies
          Applies deterministic bank fraud governance overrides
        """

        fraud_docs = self.retriever.invoke(
            "ABC Bank fraud risk policies and guidelines"
        )
        policy_context = "\n\n".join([d.page_content for d in fraud_docs])

        prompt = f"""
You are a Senior Banking Fraud Detection Officer at ABC Bank.

Below is ABC Bank's official fraud governance policy
and a transaction/customer scenario.

------------------
BANK FRAUD POLICY
------------------
{policy_context}

------------------
SCENARIO
------------------
{scenario}

Rules:
- If NO suspicious indicators exist, do NOT create false fraud risk
- Do not hallucinate fraud if not present
- Base assessment strictly on policy + evidence
- Provide clear reasoning

Return STRICT VALID JSON ONLY:

{{
 "fraud_summary": "short professional explanation",
 "fraud_patterns_detected": [],
 "suspicious_indicators": [],
 "fraud_type_classification": "Unknown | Account Takeover | Social Engineering | Transaction Fraud",
 "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
 "recommended_action": "ALLOW | BLOCK | REVIEW_REQUIRED",
 "reference_policy_source": "ABC Bank Fraud Governance Policy"
}}
"""

        result = self.run_llm(prompt)

        # =====================================================
        # 🔐 HARD FRAUD SAFETY OVERRIDES (REAL BANK LOGIC)
        # =====================================================
        if customer_profile:

            #  Fully trusted compliant customer override
            if (
                customer_profile.get("kyc_status") == "VALID"
                and customer_profile.get("risk_category", "").upper() == "LOW"
                and customer_profile.get("aml_screening_passed") is True
                and customer_profile.get("fraud_history") == "NONE"
            ):
                result["risk_level"] = "LOW"
                result["recommended_action"] = "ALLOW"
                result["fraud_summary"] = (
                    "Customer is fully KYC verified, AML cleared, "
                    "no historical fraud indicators and low inherent risk. "
                    "No suspicious activity detected."
                )
                result["suspicious_indicators"] = []
                result["fraud_patterns_detected"] = []
                return result

          
        return result
