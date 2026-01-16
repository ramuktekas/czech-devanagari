# czech_dev/softening.py

import json
from pathlib import Path

from .fronting import apply_fronting
from .base_map import BASE_MAP


# Load softening map
_SOFT_MAP = json.loads(
    (Path(__file__).parent.parent / "data" / "soft_map.json").read_text()
)


SOFTENING_VOWELS = set(_SOFT_MAP.keys())


def apply_softening(latin_tokens, dev_tokens):
    """
    Apply palatalisation / j-glide as a unified operation.

    Rule:
    - Scan for vowels: i, í, ě
    - If previous token is a consonant listed for that vowel,
      ensure halant is present on the consonant
    """

    out = dev_tokens[:]

    for i in range(1, len(latin_tokens)):
        vowel = latin_tokens[i]

        if vowel not in SOFTENING_VOWELS:
            continue

        prev = latin_tokens[i - 1]

        # Must be a consonant
        if prev not in BASE_MAP["consonants"]:
            continue

        # Must be eligible for this vowel
        if prev not in _SOFT_MAP[vowel]:
            continue

        # Apply softening (halant) to the consonant
        out[i - 1] = apply_fronting(out[i - 1])

    return out
