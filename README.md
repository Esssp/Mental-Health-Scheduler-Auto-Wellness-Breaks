# Mental Health Break Scheduler

## Project Overview
This is a FastAPI-based application that schedules mental health breaks directly into Google Calendar.  
Users can send a request with a short prompt (e.g., "Take a walk", "Meditation break") and the app will automatically create a calendar event.

## Features
- Simple API endpoint `/schedule`
- Connects with Google Calendar API
- Automatically schedules a 30-minute break event
- Secure OAuth authentication using `credentials.json`

## How to Run
1. Clone the repo or unzip the project.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
