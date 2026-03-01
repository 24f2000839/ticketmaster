from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
import re
import json
import logging

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response

@app.get("/execute")
def execute(q: str = Query(...)):

    print("\n==============================")
    print("RAW QUERY RECEIVED:", q)
    print("==============================\n")

    q_lower = q.lower()

    # 1️⃣ Ticket Status
    ticket_match = re.search(r"ticket\s+(\d+)", q_lower)
    if "status" in q_lower and ticket_match:
        result = {
            "name": "get_ticket_status",
            "arguments": json.dumps({
                "ticket_id": int(ticket_match.group(1))
            })
        }
        print("MATCHED: get_ticket_status")
        print("RETURNING:", result)
        return result

    # 2️⃣ Meeting
    meeting_match = re.search(
        r"on\s+(\d{4}-\d{2}-\d{2})\s+at\s+(\d{2}:\d{2})\s+in\s+(.+?)(?:\.|$)",
        q
    )
    if "meeting" in q_lower and meeting_match:
        result = {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": meeting_match.group(1),
                "time": meeting_match.group(2),
                "meeting_room": meeting_match.group(3)
            })
        }
        print("MATCHED: schedule_meeting")
        print("RETURNING:", result)
        return result

    # 3️⃣ Expense
    expense_match = re.search(r"employee\s+(\d+)", q_lower)
    if "expense" in q_lower and expense_match:
        result = {
            "name": "get_expense_balance",
            "arguments": json.dumps({
                "employee_id": int(expense_match.group(1))
            })
        }
        print("MATCHED: get_expense_balance")
        print("RETURNING:", result)
        return result

    # 4️⃣ Bonus
    bonus_match = re.search(r"employee\s+(\d+).*?(\d{4})", q_lower)
    if "bonus" in q_lower and bonus_match:
        result = {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(bonus_match.group(1)),
                "current_year": int(bonus_match.group(2))
            })
        }
        print("MATCHED: calculate_performance_bonus")
        print("RETURNING:", result)
        return result

    # 5️⃣ Office Issue
    issue_match = re.search(r"issue\s+(\d+)", q_lower)
    dept_match = re.search(r"for\s+the\s+(.+?)\s+department", q_lower)
    if issue_match and dept_match:
        result = {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue_match.group(1)),
                "department": dept_match.group(1).capitalize()
            })
        }
        print("MATCHED: report_office_issue")
        print("RETURNING:", result)
        return result

    print("NO MATCH FOUND")
    return {"error": "Query not recognized"}
