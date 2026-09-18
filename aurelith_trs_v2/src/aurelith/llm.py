from __future__ import annotations

import os
from dotenv import load_dotenv

load_dotenv()


class OpenAIReasoner:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model = os.getenv("AURELITH_MODEL", "gpt-5.6")

    def available(self):
        return bool(self.api_key)

    def respond(self, instructions: str, input_text: str):
        if not self.available():
            return (
                "[offline TRS mode] State persisted successfully, but no "
                "OPENAI_API_KEY is configured for language generation."
            )

        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)
        response = client.responses.create(
            model=self.model,
            instructions=instructions,
            input=input_text,
        )
        return response.output_text.strip()
