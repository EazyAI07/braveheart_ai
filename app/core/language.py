PIDGIN_KEYWORDS = [
    "dey", "wetin", "wahala", "abi", "no be", "fit", "go", "dey do"
]

def detect_language(text: str) -> str:
    text_lower = text.lower()
    for kw in PIDGIN_KEYWORDS:
        if kw in text_lower:
            return "pidgin"
    return "english"
