# src/llm/openai_client.py

import os
from typing import List, Dict, Any
from openai import OpenAI, RateLimitError
import requests

# Read flag from environment (.env)
USE_REAL_API = os.getenv("USE_REAL_API", "false").lower() == "true"

# Only create the client if we're using the real API
client = OpenAI() if USE_REAL_API else None


def ask_ai_action(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Call local Ollama (http://localhost:11434) to get an assistant reply,
    then wrap it in our action dict format.

    For now this just does simple 'chat' actions.
    """
    payload = {
    "model": os.getenv("OLLAMA_MODEL", "llama3"),
    # "llama3" will automatically use llama3:latest
    "messages": messages,
    "stream": False,
}



    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json=payload,
            timeout=60,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        # If Ollama is not running or something else failed, return an error chat
        return {
            "action": "chat",
            "task": {
                "title": None,
                "description": None,
                "due_date": None,
                "time_of_day": None,
                "recurrence": "none",
                "tags": None,
                "status": "pending",
            },
            "note": {"text": None},
            "filters": {"date": None, "range": None},
            "reply": f"Sorry, I couldn't reach the local model. Error: {e}",
            "error": "ollama_request_failed",
        }

    data = response.json()
    assistant_message = data.get("message", {}).get("content", "")

    return {
        "action": "chat",
        "task": {
            "title": None,
            "description": None,
            "due_date": None,
            "time_of_day": None,
            "recurrence": "none",
            "tags": None,
            "status": "pending",
        },
        "note": {"text": None},
        "filters": {"date": None, "range": None},
        "reply": assistant_message,
        "error": None,
    }
