from agents.base_agent import BaseAgent

class KYCAgent(BaseAgent):

    def evaluate_kyc(self, customer_profile: dict):

        policy_docs = self.retriever.invoke("ABC Bank KYC policy requirements")
        policy_context = "\n\n".join([d.page_content for d in policy_docs])

        prompt = f"""
You are a Senior Banking KYC / KYB Compliance Officer at ABC Bank.

Below is the bank's KYC policy and a customer profile.
Evaluate whether the customer is KYC compliant.

------------------
BANK POLICY DATA
------------------
{policy_context}

------------------
CUSTOMER PROFILE
------------------
{customer_profile}

Important Banking Rules:
- If customer has VALID KYC + Government ID + address + AML clear + PEP clear,
  then the customer is FULLY COMPLIANT and should be marked PASS.
- Do NOT create unnecessary risk if policy expectation is already satisfied.
- If there is no risk, do not mark MEDIUM or HIGH.
- Only mark PARTIAL / FAIL when strong evidence is missing.

Return STRICT VALID JSON ONLY:

{{
 "policy_understanding_summary": "short explanation of what policy expects",
 "kyc_checks_performed": [
   "check 1",
   "check 2"
 ],
 "missing_or_incomplete_requirements": [],
 "compliance_status": "PASS | FAIL | PARTIAL",
 "risk_level": "LOW | MEDIUM | HIGH",
 "justification": "clear banking explanation",
 "reference_policy_source": "policy file reference"
}}
"""
        result = self.run_llm(prompt)

        # -----------------------------------
        # Hard Safe Banking Logic Override
        # -----------------------------------
        if (
            customer_profile.get("kyc_status") == "VALID" and
            customer_profile.get("document_type") and
            customer_profile.get("document_number") and
            customer_profile.get("aml_screening_passed") is True and
            customer_profile.get("pep_check") == "CLEAR" and
            customer_profile.get("fraud_history") == "NONE"
        ):
            result["compliance_status"] = "PASS"
            result["risk_level"] = "LOW"
            result["justification"] = (
                "Customer has full KYC verification, valid government ID, "
                "AML screening passed, PEP cleared, no fraud history."
            )
            result["missing_or_incomplete_requirements"] = []

        return result
