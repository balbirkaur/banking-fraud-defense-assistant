import os
import sys
import json

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")
sys.path.append(ROOT)

from orchestrator import app


def test_orchestrator_streaming():

    print("\n===== LANGGRAPH STREAMING WORKFLOW =====\n")

    state = {
        "user_input": "Customer tries to transfer $15,000 to a new beneficiary.",
        "kyc_data": {
            "customer_name": "Rahul Sharma",
            "kyc_status": "VALID",
            "nationality": "Indian"
        }
    }

    # Streaming Execution
    for event in app.stream(state, stream_mode="updates"):
        for node, value in event.items():
            print(f"\n--- NODE COMPLETED: {node.upper()} ---")
            print(json.dumps(value, indent=4))

    print("\n===== STREAMING COMPLETED =====")


if __name__ == "__main__":
    test_orchestrator_streaming()
