import os
from utils.json_utils import safe_json_parse
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()


class PolicyAgent:

    def __init__(self, retriever):
        self.retriever = retriever

        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION")
        )

    def analyze_policy(self, query: str):
        docs = self.retriever.invoke(query)
        context = "\n\n".join([d.page_content for d in docs])

        prompt = f"""
You are a Senior Banking Policy Intelligence Officer for ABC Bank.

Using the below policy data, analyze and extract only relevant banking governance rules.

POLICY DATA:
{context}

Your job:
- interpret policy correctly
- do not hallucinate
- strictly use only above content
- do not assume anything

Return OUTPUT STRICTLY IN VALID JSON:

{{
 "policy_summary": "Short explanation of applicable policy in plain professional English",
 "required_conditions": [
     "condition 1",
     "condition 2",
     "condition 3"
 ],
 "restricted_actions": [
     "restricted behavior 1",
     "restricted behavior 2"
 ],
 "risk_level": "LOW | MEDIUM | HIGH",
 "reference_source": "mention which policy file or section it came from"
}}
"""

        response = self.llm.invoke(prompt)

        # Use GLOBAL enterprise JSON handler
        return safe_json_parse(response.content)