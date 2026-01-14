# czech_dev/preprocess.py

from .parser import parse
from .base_map import BASE_MAP
from .fronting import apply_fronting

HALANT = "्"


def preprocess(text: str):
    """
    Parse Czech text and normalize it into a Devanagari stream
    where:
    - all consonants carry a halant by default
    - fronting is applied to consonants (not vowels)
    - no schwa logic is applied yet
    """

    # 1. Parse Latin text
    latin_tokens = parse(text)

    # 2. Base-map Latin → Devanagari
    dev_tokens = []
    for tok in latin_tokens:
        if tok in BASE_MAP["consonants"]:
            dev = BASE_MAP["consonants"][tok]["dev"]
            dev_tokens.append(dev)
        elif tok in BASE_MAP["vowels"]:
            dev = BASE_MAP["vowels"][tok]["dev"]
            dev_tokens.append(dev)
        else:
            # punctuation, spaces, etc.
            dev_tokens.append(tok)

    # 3. Add halant to ALL consonants (default Czech state)
    for i, tok in enumerate(latin_tokens):
        if tok in BASE_MAP["consonants"]:
            dev_tokens[i] = dev_tokens[i] + HALANT

    # 4. Apply fronting to consonants (triggered by vowels)
    dev_tokens = apply_fronting(latin_tokens, dev_tokens, BASE_MAP)

    return latin_tokens, dev_tokens
