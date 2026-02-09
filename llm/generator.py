import json
import requests
from typing import Dict, List

from langchain_core.documents import Document

import re


def strip_json_comments(text: str) -> str:
    """
    Removes // style comments from JSON-like text.
    """
    return re.sub(r"//.*?$", "", text, flags=re.MULTILINE)

class LLMGenerator:
    """
    Local LLM-based generator using Ollama (non-paid).
    Produces schema-constrained, auditable COREP output.
    """

    def __init__(self, model: str = "mistral"):
        self.model = model
        self.endpoint = "http://localhost:11434/api/generate"

    def generate(
        self,
        question: str,
        scenario: str,
        retrieved_docs: List[Document],
        schema: Dict,
    ) -> Dict:

        context_text = "\n\n".join(
            f"Source: {doc.metadata.get('source')}\n{doc.page_content}"
            for doc in retrieved_docs
        )

        prompt = f"""
You are a regulatory reporting assistant for UK PRA COREP reporting.

STRICT RULES (DO NOT VIOLATE):
1. Use ONLY the regulatory context provided.
2. Populate the JSON schema EXACTLY as given.
3. Do NOT invent numeric values.
4. Populate "amount" ONLY if the reporting scenario explicitly provides a number.
5. For rule references:
   - "section" must contain the section number only (e.g. "2", "3", "4")
   - "paragraph" must contain the paragraph number only (e.g. "2.1", "3.1")
6. If a value or rule reference is unclear, leave it empty or null.
7. Output VALID JSON ONLY. No text, no explanation.

REGULATORY CONTEXT:
{context_text}

USER QUESTION:
{question}

REPORTING SCENARIO:
{scenario}

JSON SCHEMA:
{json.dumps(schema, indent=2)}

Return a valid JSON object that strictly matches the schema.
"""


        response = requests.post(
            self.endpoint,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()
        raw_output = response.json()["response"]
        # -----------------------------
        # SAFE JSON EXTRACTION (FINAL)
        # -----------------------------
        start = raw_output.find("{")
        end = raw_output.rfind("}")
        if start == -1 or end == -1:
             raise ValueError("LLM response does not contain JSON")
        json_str = raw_output[start : end + 1]
        # Remove // comments added by LLM
        json_str = strip_json_comments(json_str)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse cleaned JSON from LLM output:\n{json_str}"
            ) from e
            

      
