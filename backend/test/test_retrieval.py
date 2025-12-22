import sys, os
sys.path.append(os.path.abspath(".."))

from retriever import init_retriever

retriever = init_retriever()

query = "What are the KYC requirements in ABC Bank?"
results = retriever.invoke(query)

print("\n===== RETRIEVED RESULTS =====\n")

for i, doc in enumerate(results, start=1):
    print(f"Result {i}:")
    print(doc.page_content)
    print("-" * 60)
