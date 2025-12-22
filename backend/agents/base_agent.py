import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from utils.json_utils import safe_json_parse

load_dotenv()


class BaseAgent:

    def __init__(self, retriever=None):
        self.retriever = retriever

        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION")
        )

    def run_llm(self, prompt: str):
        """
        Common execution template:
        - sends prompt to Azure OpenAI
        - ensures JSON output
        - safe parse
        """
        response = self.llm.invoke(prompt)
        return safe_json_parse(response.content)
