import sys, os
sys.path.append(os.path.abspath(".."))

from retriever import init_retriever

from agents.policy_agent import PolicyAgent

retriever = init_retriever()

agent = PolicyAgent(retriever)

result = agent.analyze_policy("What are ABC Bank KYC policy rules?")
print(result)
