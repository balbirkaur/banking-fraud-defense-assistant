import os
import sys
import json

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")
sys.path.append(ROOT)

from orchestrator import app


def test_orchestrator():

    print("\n===== LANGGRAPH ORCHESTRATION TEST =====\n")

    state = {
        "user_input": "Customer is trying to transfer $15,000 to a newly added beneficiary.",
        "kyc_data": {
            "customer_name": "Balbir Kaur",
            "kyc_status": "VALID",
            "nationality": "Indian"
        },
        "memory": []          # <<< REQUIRED FOR SHORT-TERM MEMORY
    }

    result = app.invoke(state)

    print("\n===== FINAL ORCHESTRATION OUTPUT =====\n")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    test_orchestrator()
