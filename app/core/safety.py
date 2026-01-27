CRISIS_KEYWORDS = [
    "kill myself",
    "end my life",
    "no reason to live",
    "i want to die",
    "i don't want to wake up",
    "overdose",
    "take everything",
    "life no get meaning",
    "i tire of life",
    "make i just die"
]

def detect_crisis(text: str) -> bool:
    text_lower = text.lower()
    return any(kw in text_lower for kw in CRISIS_KEYWORDS)


def crisis_response(language="english") -> str:
    if language == "pidgin":
        return (
            "I really sorry say you dey feel like this. "
            "I no be doctor, but your life matter well well.\n\n"
            "If you fit, abeg reach out to person wey fit help you now now:\n"
            "- Call emergency services or go nearest hospital\n"
            "- Federal Neuro-Psychiatric Hospital close to you\n"
            "- Talk to trusted person (friend, family, religious leader)\n\n"
            "If you dey Lagos: 112 (emergency line)\n"
            "You no dey alone."
        )

    return (
        "I’m really sorry you’re feeling this way. "
        "I’m not a medical professional, but your life matters.\n\n"
        "Please consider reaching out for immediate help:\n"
        "- Visit the nearest hospital or emergency unit\n"
        "- Contact a Federal Neuro-Psychiatric Hospital\n"
        "- Talk to someone you trust right now\n\n"
        "If you’re in Lagos: call 112 (emergency line)\n"
        "You are not alone."
    )
