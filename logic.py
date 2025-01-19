import json
from datetime import datetime

events = {}

def add_event(date, task):
    new_task = {"task": task, "completed": False}
    if date in events:
        events[date].append(new_task)
    else:
        events[date] = [new_task]
    save_events()

def get_events(date):
    return events.get(date, [])

def remove_event(date, task_index):
    if date in events and 0 <= task_index < len(events[date]):
        events[date].pop(task_index)
        if not events[date]:
            del events[date]
    save_events()

def toggle_event(date, task_index):
    if date in events and 0 <= task_index < len(events[date]):
        events[date][task_index]["completed"] = not events[date][task_index]["completed"]
    save_events()

def save_events():
    with open("events.json", "w") as file:
        json.dump(events, file)

def load_events():
    global events
    try:
        with open("events.json", "r") as file:
            events = json.load(file)
    except FileNotFoundError:
        events = {}