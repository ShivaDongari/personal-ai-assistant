# Personal AI Assistant (Gen AI Project)

Hi, I'm **Shivakumar (Shiva) Dongari** 👋

I'm currently part of an **AI Training program**, and this repository is for my **Personal AI Assistant** project.  
The goal is to build a small but real assistant that helps reduce my mental load and can be scaled later.

---

## 1. Project Goal (MVP)

Build a **CLI-based personal AI assistant** that:

- Understands natural language like:
  - _"Remind me to pay rent on the 1st of every month"_
  - _"Add a task to study SQL for 1 hour tomorrow evening"_
- Converts that into **structured tasks/reminders** stored in a simple storage (JSON file).
- Answers questions like:
  - _"What are my tasks for tomorrow?"_
  - _"What do I need to do this weekend?"_
- Generates a **daily summary** like:
  - _"Here’s your plan for tomorrow: Morning – Gym, Afternoon – SQL practice, Evening – Call Amma"_.

This is the **Minimum Viable Product (MVP)** for my Gen AI training.

---

## 2. Gen AI Concepts Involved

This project is mainly about applying **Gen AI / LLMs** to a real problem.

Key concepts:

- **LLM Integration**  
  Use a Large Language Model (via API) to:
  - Understand user intent (create task, query tasks, ask for summary, chit-chat).
  - Extract structured data (titles, dates, tags) from natural language.

- **Prompt Engineering**  
  Design prompts that:
  - Ask the model to return **JSON** with fields like `action`, `title`, `due_date`, etc.
  - Encourage the model to choose between actions like `"create_task"`, `"query_tasks"`, `"daily_summary"`.

- **Mini-Agent Architecture**  
  Separate:
  - LLM "brain" (understanding + reasoning),
  - Task manager (business logic),
  - Storage (JSON files now, database later).

- **Data Modeling & Persistence**  
  Represent a **Task** with fields like:
  - `id`, `title`, `description`, `due_datetime`, `recurrence`, `tags`, `status`.
  Store these in `data/tasks.json`.

---

## 3. Planned Architecture (High-Level)

```text
CLI (User)  <-->  Assistant Core  <-->  LLM Client
                         |
                         v
                  Task Manager  <-->  tasks.json
                  
4. Current Status (Phase 1 – Implemented)

Right now, I have built the **foundation** of the personal AI assistant with a working CLI app and local task/notes features.

### ✅ Implemented

- **CLI Assistant**
  - Run with `python app.py`.
  - Text interface in the terminal (`You:` prompt).
  - Maintains **conversation history** (system + user + assistant messages).

- **Commands (Assistant Core)**
  - `/help` – show available commands.
  - `/clear` – clear conversation history and restart from the system prompt.
  - `/note <text>` – save a note to `notes.txt`.
  - `/notes` – list all notes.
  - `/todo <text>` – create a simple task (stored in JSON, with an ID and status).
  - `/todos` – list all tasks with status (⏳ pending / ✔️ done).
  - `/done <id>` – mark a task as done.
  - `quit` / `exit` – exit the assistant.

- **Task & Notes Storage**
  - Tasks are stored in JSON (e.g. `data/tasks.json`) via a Task Manager module.
  - Notes are stored line-by-line in `notes.txt`.
  - This matches the idea of a separate **storage layer** that can later be replaced with a database.

- **LLM Engine Wrapper (Mock Mode)**
  - `src/llm/openai_client.py` exposes a single function:
    ```python
    def ask_ai(messages) -> str:
        ...
    ```
  - Currently runs in **mock mode** (no real API calls, no cost), because of OpenAI quota/billing limits.
  - Designed so it can later call:
    - OpenAI directly, or
    - an `n8n.ai` endpoint provided by the training program.

So the current version already follows the planned architecture:

> CLI → Assistant Core (commands, history) →  
>   LLM Client (mock for now) and Task Manager (JSON storage)

and is ready for the next phase where the LLM will translate natural language into structured task actions.

---

5. How to Run (Local)

From the project root:

```bash
# (optional) activate virtual env
venv\Scripts\activate  # on Windows

# run the assistant
python app.py
