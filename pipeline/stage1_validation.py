import re

def validate_input(question):
    """Returns (is_valid, reason). Rejects empty, too-short, or non-question input."""
    if not question or not question.strip():
        return False, "empty input"
    if len(question.strip()) < 5:
        return False, "too short to be a real question"
    if not re.search(r'[a-zA-Z]', question):
        return False, "no alphabetic content"
    return True, "ok"