from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional, List

from retriever import init_retriever

from agents.policy_agent import PolicyAgent
from agents.kyc_agent import KYCAgent
from agents.security_agent import SecurityAgent
from agents.sso_agent import SSOAgent
from agents.fraud_agent import FraudAgent
from agents.transaction_agent import TransactionMonitoringAgent
from agents.decision_agent import DecisionAgent
from agents.audit_agent import AuditAgent


# ---------------------------
# Graph State + Short Term Memory
# ---------------------------

    
class BankingState(TypedDict, total=False):
    user_input: str
    kyc_data: Optional[dict]
    policy_result: Optional[dict]
    kyc_result: Optional[dict]
    security_result: Optional[dict]
    sso_result: Optional[dict]
    fraud_result: Optional[dict]
    transaction_result: Optional[dict]
    final_decision: Optional[dict]
    memory: list



# ---------------------------
# Initialize Components
# ---------------------------
retriever = init_retriever()

memory_store = []

policy_agent = PolicyAgent(retriever, memory_store)
kyc_agent = KYCAgent(retriever, memory_store)
security_agent = SecurityAgent(retriever, memory_store)
sso_agent = SSOAgent(retriever, memory_store)
fraud_agent = FraudAgent(retriever, memory_store)
transaction_agent = TransactionMonitoringAgent(retriever, memory_store)
decision_agent = DecisionAgent(memory_store)
audit_agent = AuditAgent(memory_store)



# ---------------------------
# Workflow Steps
# ---------------------------
def run_policy(state: BankingState):
    result = policy_agent.analyze_policy(state["user_input"])
    state["policy_result"] = result

    state["memory"].append(f"Policy Risk: {result.get('risk_level', 'UNKNOWN')}")
    return state


def run_kyc(state: BankingState):
    result = kyc_agent.evaluate_kyc(state["kyc_data"])
    state["kyc_result"] = result

    state["memory"].append(
        f"KYC Compliance: {result.get('compliance_status', 'UNKNOWN')}"
    )
    return state


def run_security(state: BankingState):
    result = security_agent.evaluate_security(state["user_input"])
    state["security_result"] = result

    state["memory"].append(
        f"Security Decision: {result.get('allowed_or_denied', 'UNKNOWN')}"
    )
    return state


def run_sso(state: BankingState):
    result = sso_agent.evaluate_sso(state["user_input"])
    state["sso_result"] = result

    state["memory"].append(
        f"SSO: {result.get('allowed_or_denied', 'UNKNOWN')}"
    )
    return state


def run_fraud(state: BankingState):
    result = fraud_agent.evaluate_fraud(state["user_input"])
    state["fraud_result"] = result

    state["memory"].append(
        f"Fraud Risk: {result.get('risk_level', 'UNKNOWN')}"
    )
    return state


def run_transaction(state: BankingState):
    transactions = [
        {"amount": 12000, "type": "TRANSFER"},
        {"amount": 9000, "type": "TRANSFER"}
    ]

    result = transaction_agent.monitor_transactions(transactions)
    state["transaction_result"] = result

    state["memory"].append(
        f"Transaction Alert: {result.get('alert_required', 'UNKNOWN')}"
    )
    return state


def run_decision(state: BankingState):

    result = decision_agent.final_decision(
        kyc_result=state.get("kyc_result"),
        fraud_result=state.get("fraud_result"),
        security_result=state.get("security_result"),
        sso_result=state.get("sso_result"),
        transaction_result=state.get("transaction_result"),
        policy_result=state.get("policy_result"),
        memory=state.get("memory", [])
    )

    state["final_decision"] = result

    audit_agent.generate_audit_log(
        user_input=state["user_input"],
        kyc_result=state.get("kyc_result"),
        policy_result=state.get("policy_result"),
        security_result=state.get("security_result"),
        sso_result=state.get("sso_result"),
        fraud_result=state.get("fraud_result"),
        transaction_result=state.get("transaction_result"),
        final_decision=result
    )

    return state


# ---------------------------
# Build LangGraph
# ---------------------------
graph = StateGraph(BankingState)

graph.add_node("policy", run_policy)
graph.add_node("kyc", run_kyc)
graph.add_node("security", run_security)
graph.add_node("sso", run_sso)
graph.add_node("fraud", run_fraud)
graph.add_node("transaction", run_transaction)
graph.add_node("decision", run_decision)

graph.add_edge(START, "policy")
graph.add_edge("policy", "kyc")
graph.add_edge("kyc", "security")
graph.add_edge("security", "sso")
graph.add_edge("sso", "fraud")
graph.add_edge("fraud", "transaction")
graph.add_edge("transaction", "decision")
graph.add_edge("decision", END)

app = graph.compile()
