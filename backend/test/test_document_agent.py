import sys
import os
import json

# ensure backend root in path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_ROOT = os.path.join(BASE_DIR, "..")
sys.path.append(BACKEND_ROOT)

from agents.document_agent import DocumentAgent


def test_document_agent():

    print("\n===== DOCUMENT AGENT TEST STARTED =====\n")

    # sample customer document text
    sample_document = """
    Document Type: Government ID
    Customer Name: Balbir Kaur
    DOB: 21-08-1990
    Address: 22B MG Road, Bangalore
    ID Number: IND-9988234
    Notes: Customer onboarding KYC document
    """

    # memory not mandatory for DocumentAgent currently
    agent = DocumentAgent()

    result = agent.analyze_document(sample_document)

    print("\n===== DOCUMENT AGENT OUTPUT =====\n")
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    test_document_agent()
