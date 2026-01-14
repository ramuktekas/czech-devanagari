# czech_dev/fronting.py

HALANT = "्"


def apply_fronting(token: str) -> str:
    """
    Apply fronting to a single Devanagari token.

    In this system:
    - fronting = presence of halant
    - token is assumed to be a consonant
    - if halant already present, do nothing
    """

    if token.endswith(HALANT):
        return token
    return token + HALANT


def remove_fronting(token: str) -> str:
    """
    Remove fronting from a single Devanagari token.

    This restores the inherent vowel (schwa-like behavior).

    - if token has halant → remove it
    - if not → do nothing
    """

    if token.endswith(HALANT):
        return token[:-1]
    return token
