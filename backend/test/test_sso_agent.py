import sys
import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")
sys.path.append(ROOT)

from retriever import init_retriever
from agents.sso_agent import SSOAgent


def test_sso_agent():

    print("\n===== SSO AGENT TEST =====\n")

    retriever = init_retriever()
    agent = SSOAgent(retriever)

    scenario = """
    Employee is accessing internal transaction approval dashboard from remote laptop.
    This system allows approving high value corporate banking transactions.
    """

    result = agent.evaluate_sso(scenario)

    print("\n===== SSO AGENT OUTPUT =====\n")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    test_sso_agent()
