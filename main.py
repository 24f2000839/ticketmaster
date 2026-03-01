from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str = Query(...)):

    q_lower = q.lower()

    # Ticket status
    ticket_match = re.search(r"ticket\s+(\d+)", q_lower)
    if "status" in q_lower and ticket_match:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": int(ticket_match.group(1))
            })
        }

    # Meeting
    meeting_match = re.search(
        r"on\s+(\d{4}-\d{2}-\d{2})\s+at\s+(\d{2}:\d{2})\s+in\s+(.+)",
        q
    )
    if "meeting" in q_lower and meeting_match:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": meeting_match.group(1),
                "time": meeting_match.group(2),
                "meeting_room": meeting_match.group(3).rstrip(".")
            })
        }

    # Expense
    expense_match = re.search(r"employee\s+(\d+)", q_lower)
    if "expense" in q_lower and expense_match:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": int(expense_match.group(1))
            })
        }

    # Bonus
    bonus_match = re.search(r"employee\s+(\d+).*?(\d{4})", q_lower)
    if "bonus" in q_lower and bonus_match:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(bonus_match.group(1)),
                "current_year": int(bonus_match.group(2))
            })
        }

    # Office issue
    issue_match = re.search(r"issue\s+(\d+)", q_lower)
    dept_match = re.search(r"for the\s+(.+?)\s+department", q_lower)
    if issue_match and dept_match:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue_match.group(1)),
                "department": dept_match.group(1).capitalize()
            })
        }

    # Fallback (VERY IMPORTANT)
    return {
        "name": "get_ticket_status",
        "arguments": json.dumps({"ticket_id": 0})
    }
