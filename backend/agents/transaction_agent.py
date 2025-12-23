from agents.base_agent import BaseAgent


class TransactionMonitoringAgent(BaseAgent):

    def __init__(self, retriever=None, memory=None):
        super().__init__(retriever)
        self.memory = memory if memory else []

    def monitor_transactions(self, transactions: list):
        """
        Evaluates transaction behavior and flags suspicious patterns.
        """

        policy_docs = self.retriever.invoke("ABC Bank AML transaction monitoring rules")
        policy_context = "\n\n".join([d.page_content for d in policy_docs])

        prompt = f"""
          You are a Senior AML & Transaction Monitoring Officer at ABC Bank.

          Below is bank AML & suspicious activity policy followed by a list of transactions.

          -----------------
          BANK POLICY DATA
          -----------------
          {policy_context}

          -----------------
          CUSTOMER TRANSACTIONS
          -----------------
          {transactions}

          IMPORTANT RULE:
          If this is only a policy question, a compliance conversation,
          or NO ACTUAL transaction execution is happening,
          then do NOT assume fraud or risk.
          Return LOW risk and NO alert.

          Only raise alerts if REAL suspicious transactions exist.

          Return STRICT JSON ONLY:

          {{
          "monitoring_summary": "short professional explanation",
          "detected_patterns": [],
          "suspicious_indicators": [],
          "alert_required": "YES | NO",
          "risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
          "recommended_action": "ALLOW | BLOCK | INVESTIGATE",
          "reference_policy": "policy source"
          }}
      """


        return self.run_llm(prompt)
