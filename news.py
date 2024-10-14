import requests
from datetime import date
import os
from constants import PPX

def get_prompt(summary_question: str) -> str:
    """Get the latest from perplexity.ai.

    Args:
        summary_question: The question to ask perplexity.ai.

    Returns:
        The summary of the latest news.
    """
    request_payload = {
        "model": "llama-3.1-sonar-huge-128k-online",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": summary_question},
        ],
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {PPX}",
    }

    response = requests.post("https://api.perplexity.ai/chat/completions", json=request_payload, headers=headers)
    response.raise_for_status()

    response_data = response.json()
    summary = response_data["choices"][0]["message"]["content"]
    return summary


if __name__ == "__main__":
    today = date.today()

