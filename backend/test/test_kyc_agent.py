import sys
import os
import json

# ensure backend root is available for imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_ROOT = os.path.join(BASE_DIR, "..")
sys.path.append(BACKEND_ROOT)

from retriever import init_retriever
from agents.kyc_agent import KYCAgent


def load_customer_profile():
    path = os.path.join(BACKEND_ROOT, "data", "customers", "customer_profiles.json")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["customers"][0]


def test_kyc_agent():
    print("\n===== KYC AGENT TEST =====\n")

    retriever = init_retriever()

    # shared short term memory
    memory_store = []
    memory_store.append("Policy Risk: LOW")

    agent = KYCAgent(retriever=retriever, memory=memory_store)

    customer = load_customer_profile()

    print("\n===== CUSTOMER INPUT =====\n")
    print(json.dumps(customer, indent=4))

    result = agent.evaluate_kyc(customer)

    print("\n===== KYC AGENT OUTPUT =====\n")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    test_kyc_agent()
