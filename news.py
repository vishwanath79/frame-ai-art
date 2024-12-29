"""
Module for fetching news summaries using the Perplexity API.
"""
import logging
from typing import Optional
import requests
from datetime import date
from constants import PPX

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_prompt(summary_question: str) -> Optional[str]:
    """
    Get a response from perplexity.ai for the given question.

    Args:
        summary_question: The question to ask perplexity.ai

    Returns:
        str: The summary response from the API
        None: If the request fails
    """
    try:
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

        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            json=request_payload,
            headers=headers,
            timeout=10  # Add timeout
        )
        response.raise_for_status()

        response_data = response.json()
        summary = response_data["choices"][0]["message"]["content"]
        logger.info("Successfully retrieved response from Perplexity API")
        return summary

    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
        return None
    except (KeyError, IndexError) as e:
        logger.error(f"Failed to parse API response: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in get_prompt: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    today = date.today()
    question = f"What are the major news headlines for {today}?"
    result = get_prompt(question)
    if result:
        print(f"News summary for {today}:\n{result}")

