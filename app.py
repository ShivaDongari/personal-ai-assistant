# app.py
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env (OPENAI_API_KEY, USE_REAL_API, etc.)
load_dotenv()

from src.llm.openai_client import ask_ai


SYSTEM_PROMPT = (
    "You are Shiva's personal CLI assistant running in a terminal. "
    "Be concise, helpful, and friendly."
)

NOTES_FILE = "notes.txt"
TODOS_FILE = "todos.json"


# ---------- Conversation history helpers ----------

def build_initial_messages():
    """Create a fresh conversation history starting with the system prompt."""
    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]


# ---------- Help / commands info ----------

def print_help():
    """Show available commands."""
    print("Available commands:")
    print("  /help              - Show this help message")
    print("  /clear             - Clear the conversation history")
    print("  /note <text>       - Save a note")
    print("  /notes             - Show all saved notes")
    print("  /todo <text>       - Add a todo item")
    print("  /todos             - Show all todos")
    print("  /done <number>     - Mark a todo item as done")
    print("  quit               - Exit the assistant")
    print("  exit               - Exit the assistant")
    print()


# ---------- Notes functionality ----------

def add_note(text: str):
    """Append a note to the notes file."""
    text = text.strip()
    if not text:
        print("Assistant: Cannot add an empty note. Usage: /note <your note here>\n")
        return

    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")

    print(f"Assistant: Note added ✅ ({text})\n")


def show_notes():
    """Read and print all notes."""
    if not os.path.exists(NOTES_FILE):
        print("Assistant: No notes found yet. Use /note to add one. 📝\n")
        return

    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if not lines:
        print("Assistant: No notes found yet. Use /note to add one. 📝\n")
        return

    print("Assistant: Here are your notes:")
    for idx, note in enumerate(lines, start=1):
        print(f"  {idx}. {note}")
    print()  # blank line at end


# ---------- Todos functionality ----------

def load_todos():
    """Load todos from JSON file."""
    if not os.path.exists(TODOS_FILE):
        return []

    try:
        with open(TODOS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # ensure it's a list of dicts
            if isinstance(data, list):
                return data
    except Exception:
        # if file is corrupted, start fresh
        pass

    return []


def save_todos(todos):
    """Save todos to JSON file."""
    with open(TODOS_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, ensure_ascii=False, indent=2)


def add_todo(text: str):
    """Add a new todo item."""
    text = text.strip()
    if not text:
        print("Assistant: Cannot add an empty todo. Usage: /todo <task description>\n")
        return

    todos = load_todos()
    todos.append({"text": text, "done": False})
    save_todos(todos)

    print(f"Assistant: Todo added ✅ ({text})\n")


def show_todos():
    """Display all todos with status."""
    todos = load_todos()
    if not todos:
        print("Assistant: No todos yet. Use /todo to add one. ✅\n")
        return

    print("Assistant: Here are your todos:")
    for idx, todo in enumerate(todos, start=1):
        status = "✔️" if todo.get("done") else "⏳"
        print(f"  {idx}. {status} {todo.get('text', '')}")
    print()


def mark_todo_done(index_str: str):
    """Mark a todo as done by its number."""
    index_str = index_str.strip()
    if not index_str:
        print("Assistant: Usage: /done <todo number>\n")
        return

    try:
        idx = int(index_str)
    except ValueError:
        print("Assistant: Todo number must be a valid integer. Example: /done 2\n")
        return

    todos = load_todos()
    if idx < 1 or idx > len(todos):
        print(f"Assistant: Todo #{idx} does not exist. Use /todos to see the list.\n")
        return

    todos[idx - 1]["done"] = True
    save_todos(todos)
    print(f"Assistant: Marked todo #{idx} as done ✔️ ({todos[idx - 1]['text']})\n")


# ---------- Main loop ----------

def main():
    print("🧠 Personal AI Assistant (type 'quit' to exit)")
    print("Type /help to see available commands.\n")

    # Conversation history: system + future user/assistant messages
    messages = build_initial_messages()

    while True:
        user_input = input("You: ").strip()

        # Handle exit (not a slash command, just plain words)
        if user_input.lower() in {"quit", "exit"}:
            print("Assistant: Bye! 👋")
            break

        # Handle commands starting with '/'
        if user_input.startswith("/"):
            if user_input == "/help":
                print_help()
            elif user_input == "/clear":
                messages = build_initial_messages()
                print("Assistant: Conversation history cleared. Let's start fresh! ✨\n")
            elif user_input.startswith("/note"):
                parts = user_input.split(" ", 1)
                if len(parts) == 1:
                    print("Assistant: Usage: /note <your note here>\n")
                else:
                    add_note(parts[1])
            elif user_input == "/notes":
                show_notes()
            elif user_input.startswith("/todo"):
                parts = user_input.split(" ", 1)
                if len(parts) == 1:
                    print("Assistant: Usage: /todo <task description>\n")
                else:
                    add_todo(parts[1])
            elif user_input == "/todos":
                show_todos()
            elif user_input.startswith("/done"):
                parts = user_input.split(" ", 1)
                if len(parts) == 1:
                    print("Assistant: Usage: /done <todo number>\n")
                else:
                    mark_todo_done(parts[1])
            else:
                print(f"Assistant: Unknown command '{user_input}'. Type /help for options.\n")
            # Skip sending this to the model/mock
            continue

        # 1️⃣ Add the user message to the history
        messages.append({"role": "user", "content": user_input})

        # 2️⃣ Get assistant reply using the FULL history
        reply = ask_ai(messages)

        # 3️⃣ Show reply in the CLI
        print("Assistant:", reply)
        print()

        # 4️⃣ Add assistant reply back into the history
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
