import os
import sys
import json

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")
sys.path.append(ROOT)

from agents.audit_agent import AuditAgent


def test_audit_agent():

    print("\n===== AUDIT AGENT TEST =====\n")

    agent = AuditAgent()

    user_input = "Customer transferring $15,000 to a new beneficiary."

    # Dummy sample results simulating other agents
    policy_result = {"risk_level": "LOW"}
    kyc_result = {"compliance_status": "PASS"}
    security_result = {"allowed_or_denied": "ALLOW"}
    sso_result = {"allowed_or_denied": "ALLOW"}
    fraud_result = {"risk_level": "MEDIUM"}
    transaction_result = {"alert_required": "NO"}

    final_decision = {
        "final_decision": "REVIEW_REQUIRED",
        "final_risk_level": "MEDIUM",
        "human_review_required": True
    }

    result = agent.generate_audit_log(
        user_input=user_input,
        kyc_result=kyc_result,
        policy_result=policy_result,
        security_result=security_result,
        sso_result=sso_result,
        fraud_result=fraud_result,
        transaction_result=transaction_result,
        final_decision=final_decision
    )

    print("===== GENERATED AUDIT RECORD =====\n")
    print(json.dumps(result, indent=4))

    # Validate file exists
    log_path = os.path.join(ROOT, "logs", "audit_logs.jsonl")

    if os.path.exists(log_path):
        print("\nAudit log successfully written to:", log_path)
    else:
        print("\nERROR: Audit log file not found!")


if __name__ == "__main__":
    test_audit_agent()
