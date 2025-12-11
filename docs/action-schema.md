# Action Schema for Personal AI Assistant

The LLM must **always** respond with a single JSON object.

## Top-level structure

```json
{
  "action": "create_task | list_tasks | add_note | list_notes | daily_summary | chat",
  "task": {
    "title": "Pay rent",
    "description": "Apartment rent",
    "due_date": "2025-01-01",
    "time_of_day": "morning",
    "recurrence": "once | daily | weekly | monthly | yearly | none",
    "tags": ["finance", "home"],
    "status": "pending"
  },
  "note": {
    "text": "Call dentist about follow-up"
  },
  "filters": {
    "date": "2025-01-01",
    "range": "today | tomorrow | this_week | next_week | this_month | all"
  },
  "reply": "Natural language reply the assistant should say to the user.",
  "error": null
}
