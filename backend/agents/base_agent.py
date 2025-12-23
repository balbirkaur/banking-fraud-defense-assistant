import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from agents.utils.json_utils import safe_json_parse

load_dotenv()


class BaseAgent:

    def __init__(self, retriever=None, memory=None):
        self.retriever = retriever
        self.memory = memory if memory is not None else []

        # Enable streaming capability
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            streaming=True
        )

    def run_llm(self, prompt: str):
        """
        Normal execution:
        - Sends prompt
        - Waits for full response
        - Parses JSON safely
        """
        response = self.llm.invoke(prompt)
        return safe_json_parse(response.content)
    
    def remember(self, entry: str):
        """Short term memory append"""
        self.memory.append(entry)

    def stream_llm(self, prompt: str):
        """
        Streaming execution:
        - Streams token output live
        - Prints partial response in console
        - After streaming completes, joins text
        - Parses final JSON safely
        """

        chunks = []
        print("\n--- STREAMING STARTED ---\n")

        for chunk in self.llm.stream(prompt):
            text = chunk.content or ""
            print(text, end="", flush=True)
            chunks.append(text)

        print("\n\n--- STREAMING COMPLETED ---\n")

        final_text = "".join(chunks)
        return safe_json_parse(final_text)
