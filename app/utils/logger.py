import datetime

def log_event(event: str):
    timestamp = datetime.datetime.utcnow().isoformat()
    print(f"[{timestamp}] {event}")
