import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://candidate-llm.extraction.artificialos.com/v1/responses"
DEFAULT_MODEL = "gpt-5-mini-2025-08-07"
TIMEOUT = 30

# Large enough for reasoning + final answer
DEFAULT_MAX_OUTPUT_TOKENS = 512
MAX_RETRIES = 3
MAX_HARD_LIMIT = 4096


class LLMClient:
    """
    Wrapper for Artificial's Responses API with:
    - Environment-based API key
    - Safe token defaults
    - Retry on 'max_output_tokens' incomplete errors
    - Robust parsing of the 'output' structure
    """

    def __init__(self, model: str = DEFAULT_MODEL):
        api_key = os.getenv("CANDIDATE_API_KEY")
        if not api_key:
            raise ValueError(
                "CANDIDATE_API_KEY is not set. "
                "Set it in your environment or .env file."
            )
        self.api_key = api_key
        self.model = model

    def ask(self, messages, max_output_tokens: int = DEFAULT_MAX_OUTPUT_TOKENS) -> str:
        """
        Call the Responses API with a list of messages:
            [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]

        Automatically retries if the response is 'incomplete' due to max_output_tokens.
        Returns the first text segment from the 'output' list.
        """
        tokens = max(128, max_output_tokens or DEFAULT_MAX_OUTPUT_TOKENS)
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
        }

        for attempt in range(MAX_RETRIES):
            if tokens > MAX_HARD_LIMIT:
                tokens = MAX_HARD_LIMIT

            payload = {
                "model": self.model,
                "input": messages,
                "max_output_tokens": tokens,
            }

            resp = requests.post(
                BASE_URL, json=payload, headers=headers, timeout=TIMEOUT
            )

            if resp.status_code != 200:
                raise RuntimeError(f"API error {resp.status_code}: {resp.text}")

            data = resp.json()

            status = data.get("status")
            if status and status != "completed":
                reason = (data.get("incomplete_details") or {}).get("reason")
                # If we hit the token limit, retry with more
                if reason == "max_output_tokens" and attempt < MAX_RETRIES - 1:
                    tokens = min(tokens * 2, MAX_HARD_LIMIT)
                    continue
                raise RuntimeError(
                    f"LLM response not completed. status={status}, "
                    f"details={data.get('incomplete_details')}"
                )

            # Try to parse output[*].content[*].text
            outputs = data.get("output", [])
            for item in outputs:
                content_list = item.get("content") or []
                for c in content_list:
                    text = c.get("text")
                    if isinstance(text, str):
                        return text.strip()

            # Fallback: some variants expose text here
            text_block = data.get("text", {}).get("content")
            if isinstance(text_block, str):
                return text_block.strip()

            # If we get here, structure is unexpected
            raise RuntimeError(f"Unexpected API output structure: {data}")

        raise RuntimeError("LLM ask() failed after retries.")
