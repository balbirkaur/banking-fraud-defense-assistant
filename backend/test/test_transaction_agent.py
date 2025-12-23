import sys
import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")
sys.path.append(ROOT)

from retriever import init_retriever
from agents.transaction_agent import TransactionMonitoringAgent


def test_transaction_agent():
    print("\n===== TRANSACTION MONITORING TEST =====\n")

    retriever = init_retriever()

    # shared short-term memory
    memory_store = []
    memory_store.append("Previous fraud level: LOW")

    agent = TransactionMonitoringAgent(retriever, memory_store)

    transactions = [
        {"amount": 12000, "type": "TRANSFER", "recipient": "NEW_BENEFICIARY"},
        {"amount": 9800, "type": "TRANSFER", "recipient": "NEW_BENEFICIARY"},
        {"amount": 15000, "type": "CASH_WITHDRAWAL"},
        {"amount": 200, "type": "POS_PURCHASE"}
    ]

    result = agent.monitor_transactions(transactions)

    print("\n===== TRANSACTION MONITORING OUTPUT =====\n")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    test_transaction_agent()
