from agents.base_agent import BaseAgent


class DecisionAgent(BaseAgent):

   def final_decision(
    self,
    kyc_result=None,
    fraud_result=None,
    security_result=None,
    sso_result=None,
    transaction_result=None,
    policy_result=None,
    memory=None
):
        """
        Combines outputs from multiple agents and decides
        whether banking operation should be ALLOWED / BLOCKED / REVIEW_REQUIRED
        """
        memory = memory or []
        decision_reasons = []
        final_status = "ALLOW"
        final_risk = "LOW"

        # =========================
        # 1️⃣ POLICY CHECK
        # =========================
        if policy_result:
            if policy_result.get("risk_level") in ["HIGH", "CRITICAL"]:
                final_status = "REVIEW_REQUIRED"
                final_risk = "HIGH"
                decision_reasons.append("Policy indicates high risk")

        # =========================
        # 2️⃣ KYC CHECK
        # =========================
        if kyc_result:
            if kyc_result.get("compliance_status") in ["FAIL", "PARTIAL"]:
                final_status = "REVIEW_REQUIRED"
                final_risk = "HIGH"
                decision_reasons.append("KYC not fully compliant")

        # =========================
        # 3️⃣ SECURITY CHECK
        # =========================
        if security_result:
            if security_result.get("allowed_or_denied") == "DENY":
                final_status = "DENY"
                final_risk = "HIGH"
                decision_reasons.append("Security policy denied the action")

        # =========================
        # 4️⃣ SSO / AUTH CHECK
        # =========================
        if sso_result:
            if sso_result.get("allowed_or_denied") == "DENY":
                final_status = "DENY"
                final_risk = "HIGH"
                decision_reasons.append("SSO / Authentication not compliant")

        # =========================
        # 5️⃣ FRAUD CHECK
        # =========================
        if fraud_result:
            if fraud_result.get("risk_level") in ["HIGH", "CRITICAL"]:
                final_status = "BLOCK"
                final_risk = "CRITICAL"
                decision_reasons.append("Fraud risk detected")

        # =========================
        # 6️⃣ TRANSACTION CHECK
        # =========================
        if transaction_result:
            if transaction_result.get("alert_required") == "YES":
                final_status = "REVIEW_REQUIRED"
                final_risk = "HIGH"
                decision_reasons.append("Suspicious transaction behavior detected")

        # If no reasons added → everything good
        if not decision_reasons:
            decision_reasons.append("All checks passed successfully")

        return {
            "final_decision": final_status,
            "final_risk_level": final_risk,
            "decision_reasons": decision_reasons,
            "human_review_required": final_status in ["REVIEW_REQUIRED", "DENY", "BLOCK"]
        }
