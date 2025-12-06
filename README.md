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
