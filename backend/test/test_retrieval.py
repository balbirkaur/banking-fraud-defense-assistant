import sys
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(BASE, "..")
sys.path.append(ROOT)

from retriever import init_retriever


def test_retriever():
    retriever = init_retriever()

    query = "What are the KYC requirements in ABC Bank?"
    results = retriever.invoke(query)

    print("\n===== RETRIEVED RESULTS =====\n")

    for i, doc in enumerate(results, start=1):
        print(f"Result {i}:")
        print(doc.page_content)
        print("-" * 80)


if __name__ == "__main__":
    test_retriever()
