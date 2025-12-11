# src/llm/openai_client.py

import os
from typing import List, Dict, Any
from openai import OpenAI, RateLimitError

# Read flag from environment (.env)
USE_REAL_API = os.getenv("USE_REAL_API", "false").lower() == "true"

# Only create the client if we're using the real API
client = OpenAI() if USE_REAL_API else None


def ask_ai(messages: List[Dict[str, str]]) -> str:
    """
    Takes a full chat history (list of {'role', 'content'}) and returns
    the assistant's next reply as plain text.

    If USE_REAL_API is false, returns a mock reply instead of calling OpenAI.
    """

    # 1) MOCK MODE – no real API calls
    if not USE_REAL_API:
        # Find the last user message for a nicer mock response
        last_user_msg = None
        for msg in reversed(messages):
            if msg.get("role") == "user":
                last_user_msg = msg.get("content")
                break

        if last_user_msg is None:
            last_user_msg = "(no user message found)"

        history_length = len([m for m in messages if m["role"] in ("user", "assistant")])

        return (
            "[mock reply]\n"
            f"Last thing you said: {last_user_msg}\n"
            f"Conversation turns so far: {history_length}\n\n"
            "In real mode, I would use the full history you sent to generate a contextual reply. 🙂"
        )

    # 2) REAL API MODE – actually call OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        return response.choices[0].message.content

    except RateLimitError:
        return "⚠️ API quota exceeded. Please check your OpenAI billing/usage."

    except Exception as e:
        return f"Unexpected error: {e}"
def ask_ai_action(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    TEMP simple version: no real AI logic yet.
    It just returns a 'chat' action echoing the last user message.
    We'll upgrade this later to use a system prompt and real JSON schema.
    """
    last_user_message = messages[-1]["content"]

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
        "reply": f"(Action mode) You said: {last_user_message}",
        "error": None,
    }
