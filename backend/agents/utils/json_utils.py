import re
import json


def extract_json_block(text: str) -> str:
    """
    Cleans Azure OpenAI / LLM outputs and extracts valid JSON content.
    Handles:
    - ```json fences
    - ``` fences
    - leading text
    - trailing explanations
    - whitespace
    """

    if not text:
        return "{}"

    # remove markdown fences
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

    # find JSON block
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        return "{}"

    return text[start:end + 1]


def safe_json_parse(text: str):
    """
    Safely parse JSON content.
    Returns:
    - parsed json dict
    - OR structured failure output
    """

    try:
        cleaned = extract_json_block(text)
        return json.loads(cleaned)

    except Exception as e:
        return {
            "error": "JSON parse failed",
            "reason": str(e),
            "raw_response": text
        }
