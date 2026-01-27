from collections import deque
from time import time

SESSION_TTL = 1800 
MAX_TURNS = 3

_sessions = {}

def get_session(session_id: str):
    session = _sessions.get(session_id)
    if not session:
        return None
    if time() - session["last_seen"] > SESSION_TTL:
        del _sessions[session_id]
        return None
    return session["history"]

def update_session(session_id: str, user, bot):
    history = _sessions.get(session_id, {}).get("history", deque(maxlen=MAX_TURNS))
    history.append({"user": user, "bot": bot})

    _sessions[session_id] = {
        "history": history,
        "last_seen": time()
    }
