import sys
import os
import json
from retriever import init_retriever
from agents.kyc_agent import KYCAgent

# ensure backend root is available for imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_ROOT = os.path.join(BASE_DIR, "..")
sys.path.append(BACKEND_ROOT)


def load_customer_profile():
    path = "data/customers/customer_profiles.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["customers"][0]

def test_kyc_agent():
    retriever = init_retriever()
    agent = KYCAgent(retriever=retriever)

    customer = load_customer_profile()

    print("\nCUSTOMER:")
    print(customer)

    print("\nRESULT:")
    result = agent.evaluate_kyc(customer)
    print(result)

if __name__ == "__main__":
    test_kyc_agent()
