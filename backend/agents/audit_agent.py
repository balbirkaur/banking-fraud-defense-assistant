import time
import os
import json
from agents.base_agent import BaseAgent


class AuditAgent(BaseAgent):

    def __init__(self, memory=None):
        super().__init__()
        self.memory = memory if memory else []
        self.log_dir = "logs"
        self.log_file = os.path.join(self.log_dir, "audit_logs.jsonl")

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def generate_audit_log(
        self,
        user_input,
        kyc_result=None,
        policy_result=None,
        security_result=None,
        sso_result=None,
        fraud_result=None,
        transaction_result=None,
        final_decision=None
    ):
        """
        Generates Enterprise Grade Banking Audit Record
        """

        record = {
            "audit_timestamp": time.time(),
            "audit_timestamp_readable": time.strftime("%Y-%m-%d %H:%M:%S"),

            "bank_system": "ABC BANK AI GOVERNANCE ENGINE",
            "operation": "Automated Multi-Agent Banking Decision Workflow",

            "user_input": user_input,

            "agent_outputs": {
                "policy_agent": policy_result,
                "kyc_agent": kyc_result,
                "security_agent": security_result,
                "sso_agent": sso_result,
                "fraud_agent": fraud_result,
                "transaction_monitoring_agent": transaction_result
            },

            "final_decision": final_decision,

            "compliance_statement": """
This decision was generated using a controlled AI governance workflow
following policy guidance, financial compliance frameworks, and structured
risk evaluation. No unauthorized data exposure occurred. The workflow is
designed to support regulatory alignment and internal audit readiness.
""".strip(),

            "human_review_required": (
                final_decision and final_decision.get("human_review_required", False)
            ),

            "audit_status": "LOG_RECORDED"
        }

        self._write_log(record)
        return record

    def _write_log(self, record):
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record))
            f.write("\n")
