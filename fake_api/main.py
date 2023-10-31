from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from icecream import ic
from itertools import count
from typing import Dict

from models import Alarm

app = FastAPI()
templates = Jinja2Templates(directory="templates")

counter = count(start=1)
alarms = []


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "welcome to testing API"}


@app.get("/alarms/", response_class=HTMLResponse)
async def read_items(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("alarms.html", {"request": request, "alarms": alarms})


@app.post("/alarms/", status_code=status.HTTP_201_CREATED)
async def create_alarm(alarm: Alarm) -> Alarm:
    alarm.id = next(counter)
    if alarm.id % 16 == 0:
        alarms.clear()
    alarms.append(alarm)
    ic(alarm)
    return alarm
    