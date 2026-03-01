from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import re
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/execute")
def execute(q: str = Query(...)):

    q_lower = q.lower()

    # 1️⃣ Ticket Status
    if "ticket" in q_lower and "status" in q_lower:
        match = re.search(r"ticket\s+(\d+)", q_lower)
        if match:
            ticket_id = int(match.group(1))
            return {
                "name": "get_ticket_status",
                "arguments": json.dumps({
                    "ticket_id": ticket_id
                })
            }

    # 2️⃣ Schedule Meeting
    if "schedule" in q_lower and "meeting" in q_lower:
        match = re.search(
            r"on\s+(\d{4}-\d{2}-\d{2})\s+at\s+(\d{2}:\d{2})\s+in\s+(.+)",
            q,
        )
        if match:
            date = match.group(1)
            time = match.group(2)
            meeting_room = match.group(3).rstrip(".")
            return {
                "name": "schedule_meeting",
                "arguments": json.dumps({
                    "date": date,
                    "time": time,
                    "meeting_room": meeting_room
                })
            }

    # 3️⃣ Expense Balance
    if "expense" in q_lower and "employee" in q_lower:
        match = re.search(r"employee\s+(\d+)", q_lower)
        if match:
            employee_id = int(match.group(1))
            return {
                "name": "get_expense_balance",
                "arguments": json.dumps({
                    "employee_id": employee_id
                })
            }

    # 4️⃣ Performance Bonus
    if "bonus" in q_lower:
        match = re.search(r"employee\s+(\d+).*?(\d{4})", q_lower)
        if match:
            employee_id = int(match.group(1))
            current_year = int(match.group(2))
            return {
                "name": "calculate_performance_bonus",
                "arguments": json.dumps({
                    "employee_id": employee_id,
                    "current_year": current_year
                })
            }

    # 5️⃣ Office Issue
    if "issue" in q_lower and "department" in q_lower:
        issue_match = re.search(r"issue\s+(\d+)", q_lower)
        dept_match = re.search(r"for the\s+(.+?)\s+department", q_lower)

        if issue_match and dept_match:
            issue_code = int(issue_match.group(1))
            department = dept_match.group(1).capitalize()
            return {
                "name": "report_office_issue",
                "arguments": json.dumps({
                    "issue_code": issue_code,
                    "department": department
                })
            }

    return {"error": "Query not recognized"}
