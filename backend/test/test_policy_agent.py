import sys
import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")
sys.path.append(ROOT)

from retriever import init_retriever
from agents.policy_agent import PolicyAgent


def test_policy_agent():
    print("\n===== POLICY AGENT TEST =====\n")

    retriever = init_retriever()

    # Shared short-term memory
    memory_store = []
    memory_store.append("Previous checks indicate LOW policy risk")

    agent = PolicyAgent(retriever, memory_store)

    query = "What are ABC Bank KYC policy rules?"
    result = agent.analyze_policy(query)

    print("\n===== POLICY AGENT OUTPUT =====\n")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    test_policy_agent()
