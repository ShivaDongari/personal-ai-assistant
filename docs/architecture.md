# Architecture Overview

The Personal AI Assistant is organized into three main layers:

1. User Interface (CLI)
2. Assistant Logic & Features
3. LLM Engine Wrapper

This document describes responsibilities, data flow, and extension points.

---

## Project layout (relevant files)

- `app.py` — CLI, main loop, assistant behaviors (commands, notes, todos, history)
- `notes.txt` — persistent notes (plain text)
- `todos.json` — persistent todos (JSON)
- `src/llm/openai_client.py` — LLM wrapper exposing `ask_ai`

---

## 1. User Interface (CLI)

- Implemented in `app.py`.
- Minimal I/O: `input()` for user messages, `print()` for assistant replies.
- Provides a REPL loop that exits on `quit` / `exit`.
- Translates raw user input into assistant actions or messages passed to the LLM layer.

---

## 2. Assistant Logic & Features

Located in `app.py` but conceptually separate from I/O. Responsibilities:

- Conversation history
    - Stored as `messages: List[Dict[str,str]]` (system / user / assistant).
    - Sent to `ask_ai(messages)` for AI responses.
    - `/clear` resets history to the initial system prompt.

- Commands & tools
    - `/help` — list supported commands.
    - `/clear` — clear conversation history.
    - `/note <text>` — append a note to `notes.txt`.
    - `/notes` — display notes.
    - `/todo add <text>` — add todo to `todos.json`.
    - `/todos` — list todos.
    - `/done <id>` — mark todo done (update `todos.json`).

Design principles:
- Keep assistant behaviors isolated from LLM calls so features can evolve without changing the engine wrapper.
- Persist simple data in small files for simplicity and portability.

---

## 3. LLM Engine Wrapper

File: `src/llm/openai_client.py`

- Exposes a single function:

    ```python
    def ask_ai(messages: List[Dict[str, str]]) -> str:
            ...
    ```

- Responsibilities:
    - Translate the `messages` list into the provider API call.
    - Handle API keys, retries, rate limits, and basic error handling.
    - Return assistant text as a string (no file or CLI side effects).
- Keep this layer thin and focused on communication with the LLM provider.

---

## Message format (convention)

Each message is a dict:
- role: `"system" | "user" | "assistant"`
- content: string

Example:
{
    "role": "system",
    "content": "You are a helpful assistant."
}
{
    "role": "user",
    "content": "Summarize the project architecture."
}

Pass the full `messages` list to `ask_ai`.

---

## Extension points

- Add new commands in `app.py` as pure functions that manipulate `messages` or persistent files.
- Add a higher-level service layer (e.g., `services/notes.py`, `services/todos.py`) to move logic out of `app.py` when needed.
- Swap or mock `ask_ai` for testing by providing the same signature.

---

## Testing & local development

- Keep `ask_ai` pluggable so tests can mock responses.
- Use small unit tests for command handlers (notes/todos/history).
- Run CLI manually to exercise end-to-end behavior.

---

## Security & config

- Load API keys from environment variables (do not hardcode).
- Validate and sanitize user inputs for file operations (avoid path traversal).
- Limit persisted file permissions and avoid storing secrets in plaintext.

---

This design favors simplicity and clear separation between UI, behaviors, and the LLM interface, enabling incremental enhancement without cross-cutting changes.