import json
import os


DATA_PATH = os.path.join("data", "customers", "customer_profiles.json")


def load_customers():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data["customers"]


def search_customers(query: str):
    customers = load_customers()
    q = query.lower()

    results = []

    for c in customers:
        if (
            q in c.get("customer_name", "").lower()
            or q in c.get("email", "").lower()
            or q in c.get("customer_id", "").lower()
        ):
            results.append(
                {
                    "customer_id": c.get("customer_id"),
                    "customer_name": c.get("customer_name"),
                    "email": c.get("email"),
                    "kyc_status": c.get("kyc_status", "UNKNOWN"),
                    "risk_category": c.get("risk_category", "UNKNOWN"),
                }
            )

    return results
