from datetime import datetime, timedelta
import os
import pickle

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

app = FastAPI()

def get_calendar_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)

class ScheduleRequest(BaseModel):
    prompt: str

class EventData(BaseModel):
    event_title: str
    start_time: str
    duration: int

def parse_prompt(prompt: str) -> EventData:
    now = datetime.utcnow()
    if "stretch" in prompt.lower():
        return EventData(
            event_title="Stretch Break",
            start_time=(now + timedelta(minutes=5)).isoformat(),
            duration=10
        )
    if "drink water" in prompt.lower():
        return EventData(
            event_title="Hydration Break",
            start_time=(now + timedelta(minutes=2)).isoformat(),
            duration=5
        )
    # Default fallback
    return EventData(
        event_title="Wellness Break",
        start_time=(now + timedelta(minutes=1)).isoformat(),
        duration=15
    )

@app.post("/schedule")
def schedule_break(req: ScheduleRequest):
    try:
        # Parse request
        event_data = parse_prompt(req.prompt)

        service = get_calendar_service()

        start_dt = datetime.fromisoformat(event_data.start_time)
        end_dt = start_dt + timedelta(minutes=event_data.duration)

        event = {
            "summary": event_data.event_title,
            "start": {"dateTime": start_dt.isoformat() + "Z", "timeZone": "UTC"},
            "end": {"dateTime": end_dt.isoformat() + "Z", "timeZone": "UTC"},
        }

        created_event = service.events().insert(calendarId="primary", body=event).execute()

        return {"status": "success", "link": created_event.get("htmlLink")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))