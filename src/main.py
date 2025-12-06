from llm.openai_client import get_assistant_reply


def main():
    print("👋 Welcome to Shiva's Personal AI Assistant (LLM-powered MVP)")
    print("Type 'exit' or 'quit' to close the assistant.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Assistant: Bye! 👋")
            break

        try:
            reply = get_assistant_reply(user_input)
        except Exception as e:
            print(f"Assistant (error): Something went wrong talking to the LLM: {e}")
            continue

        print(f"Assistant: {reply}\n")


if __name__ == "__main__":
    main()
from openai import OpenAI, RateLimitError

client = OpenAI()

def ask_ai(user_message: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Shiva's personal CLI assistant."},
                {"role": "user", "content": user_message},
            ],
        )
        return response.choices[0].message.content
    except RateLimitError:
        return "⚠️ API quota exceeded. Please check your OpenAI billing/usage."
    except Exception as e:
        return f"Unexpected error: {e}"

