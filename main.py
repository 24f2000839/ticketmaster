from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "API is running"}

@app.head("/")
def root_head():
    return {"status": "API is running"}

@app.get("/execute")
def execute(q: str = Query(...)):

    q_lower = q.lower().strip()

    # 1️⃣ Ticket Status
    ticket_match = re.search(r"ticket\s+(\d+)", q_lower)
    if ticket_match and "status" in q_lower:
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": int(ticket_match.group(1))
            })
        }

    # 2️⃣ Schedule Meeting
    meeting_match = re.search(
        r"on\s+(\d{4}-\d{2}-\d{2})\s+at\s+(\d{2}:\d{2})\s+in\s+(room\s+[a-z0-9]+)",
        q_lower
    )
    if meeting_match:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": meeting_match.group(1),
                "time": meeting_match.group(2),
                "meeting_room": meeting_match.group(3).title()
            })
        }

    # 3️⃣ Expense Balance
    expense_match = re.search(r"employee\s+(\d+)", q_lower)
    if expense_match and "expense" in q_lower:
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": int(expense_match.group(1))
            })
        }

    # 4️⃣ Performance Bonus
    bonus_match = re.search(r"employee\s+(\d+).*?(\d{4})", q_lower)
    if bonus_match and "bonus" in q_lower:
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(bonus_match.group(1)),
                "current_year": int(bonus_match.group(2))
            })
        }

    # 5️⃣ Office Issue
    issue_match = re.search(r"issue\s+(\d+)", q_lower)
    dept_match = re.search(r"for\s+the\s+(.+?)\s+department", q_lower)
    if issue_match and dept_match:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue_match.group(1)),
                "department": dept_match.group(1).title()
            })
        }

    return {"error": "Query not recognized"}
