import os
from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env file into environment
load_dotenv()

# Read the API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. "
        "Create a .env file in the project root with OPENAI_API_KEY=your_key_here"
    )

# Create a reusable OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are Shiva's personal AI assistant running in a CLI.
You are helpful, concise, and friendly.

Right now your main job is just to chat.
Later, you will also help with tasks and reminders.
Do NOT mention APIs or JSON, just talk naturally to the user.
""".strip()


def get_assistant_reply(user_message: str) -> str:
    """
    Send the user message to the OpenAI chat model and
    return the assistant's reply as plain text.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # you can change the model name if needed
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content.strip()
