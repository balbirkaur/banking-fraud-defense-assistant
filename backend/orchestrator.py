from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Optional

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
# Graph State
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


retriever = init_retriever()

policy_agent = PolicyAgent(retriever)
kyc_agent = KYCAgent(retriever)
security_agent = SecurityAgent(retriever)
sso_agent = SSOAgent(retriever)
fraud_agent = FraudAgent(retriever)
transaction_agent = TransactionMonitoringAgent(retriever)
decision_agent = DecisionAgent()
audit_agent = AuditAgent()



# ---------------------------
# Workflow Steps
# ---------------------------
def run_policy(state: BankingState):
    result = policy_agent.analyze_policy(state["user_input"])
    state["policy_result"] = result
    return state


def run_kyc(state: BankingState):
    result = kyc_agent.evaluate_kyc(state["kyc_data"])
    state["kyc_result"] = result
    return state


def run_security(state: BankingState):
    result = security_agent.evaluate_security(
        state["user_input"]
    )

    state["security_result"] = result
    return state



def run_sso(state: BankingState):
    result = sso_agent.evaluate_sso(state["user_input"])
    state["sso_result"] = result
    return state


def run_fraud(state: BankingState):
    result = fraud_agent.evaluate_fraud(state["user_input"])
    state["fraud_result"] = result
    return state


def run_transaction(state: BankingState):
    transactions = [
        {"amount": 12000, "type": "TRANSFER"},
        {"amount": 9000, "type": "TRANSFER"}
    ]
    result = transaction_agent.monitor_transactions(transactions)
    state["transaction_result"] = result
    return state


def run_decision(state: BankingState):

    result = decision_agent.final_decision(
        kyc_result=state.get("kyc_result"),
        fraud_result=state.get("fraud_result"),
        security_result=state.get("security_result"),
        sso_result=state.get("sso_result"),
        transaction_result=state.get("transaction_result"),
        policy_result=state.get("policy_result"),
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
