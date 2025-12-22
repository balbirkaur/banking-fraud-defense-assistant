from agents.base_agent import BaseAgent


class DocumentAgent(BaseAgent):

    def analyze_document(self, document_text: str):
        """
        Reads customer / banking documents and extracts:
        - key details
        - validation issues
        - missing fields
        - potential fraud risk indicators
        """

        prompt = f"""
You are a Senior Banking Document Intelligence Officer.

You will analyze the following document content and extract structured understanding.

DOCUMENT CONTENT:
{document_text}

Rules:
- Do NOT assume information
- Only use information present
- Identify clarity & completeness
- Identify potential fraud or suspicious indicators
- Respond ONLY based on document content

Return STRICT VALID JSON ONLY:

{{
 "document_summary": "Professional explanation of what this document represents",
 "extracted_fields": {{
      "customer_name": "",
      "dob_or_incorporation_date": "",
      "address": "",
      "document_type": "",
      "id_or_reference_number": ""
 }},
 "missing_or_incomplete_info": [
     "field 1",
     "field 2"
 ],
 "policy_violations_detected": [
     "violation 1",
     "violation 2"
 ],
 "fraud_risk_signals": [
     "signal 1",
     "signal 2"
 ],
 "risk_level": "LOW | MEDIUM | HIGH",
 "confidence_score": "0 - 100"
}}
"""

        # Use common execution template from BaseAgent
        return self.run_llm(prompt)
