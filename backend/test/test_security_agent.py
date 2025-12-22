import sys
import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")
sys.path.append(ROOT)

from retriever import init_retriever
from agents.security_agent import SecurityAgent


def test_security_agent():
    print("\n===== SECURITY AGENT TEST =====\n")

    retriever = init_retriever()
    agent = SecurityAgent(retriever)

    query = "Can we share customer KYC PDF document over email to third party vendor?"

    result = agent.evaluate_security(query)

    print("\n===== SECURITY AGENT OUTPUT =====\n")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    test_security_agent()
