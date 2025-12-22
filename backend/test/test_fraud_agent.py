import sys
import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")
sys.path.append(ROOT)

from retriever import init_retriever
from agents.fraud_agent import FraudAgent


def test_fraud_agent():

    print("\n===== FRAUD AGENT TEST =====\n")

    retriever = init_retriever()
    agent = FraudAgent(retriever)

    scenario = """
    Customer is trying to transfer $15,000 to a newly added beneficiary
    within 5 minutes of account login.
    Customer also recently changed phone number and email.
    """

    result = agent.evaluate_fraud(scenario)

    print("\n===== FRAUD AGENT OUTPUT =====\n")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    test_fraud_agent()
