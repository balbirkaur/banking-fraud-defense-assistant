import sys
import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")
sys.path.append(ROOT)

from agents.decision_agent import DecisionAgent


def test_decision_agent_pass():
    print("\n===== DECISION ENGINE TEST (PASS CASE) =====\n")

    # short-term memory store
    memory_store = []
    memory_store.append("Policy Risk: LOW")
    memory_store.append("Fraud Risk: LOW")

    agent = DecisionAgent(memory_store)

    # Simulated successful outputs from agents
    kyc = {"compliance_status": "PASS"}
    fraud = {"risk_level": "LOW"}
    security = {"allowed_or_denied": "ALLOW"}
    sso = {"allowed_or_denied": "ALLOW"}
    transaction = {"alert_required": "NO"}
    policy = {"risk_level": "LOW"}

    result = agent.final_decision(
        kyc_result=kyc,
        fraud_result=fraud,
        security_result=security,
        sso_result=sso,
        transaction_result=transaction,
        policy_result=policy
    )

    print("\n===== FINAL PASS DECISION OUTPUT =====\n")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    test_decision_agent_pass()
