# czech_dev/render.py

import json
from pathlib import Path

HALANT = "्"

# Independent vowel → dependent matra
VOWEL_TO_MATRA = {
    "अ": "",
    "आ": "ा",
    "इ": "ि",
    "ई": "ी",
    "ए": "े",
    "ऐ": "ै",
    "ओ": "ो",
    "औ": "ौ",
    "उ": "ु",
    "ऊ": "ू"
}

# Load softening map
_SOFT_MAP = json.loads(
    (Path(__file__).parent.parent / "data" / "soft_map.json").read_text()
)

SOFTENING_VOWELS = set(_SOFT_MAP.keys())


def render(tokens, latin_tokens=None):
    """
    Render internal Devanagari tokens into Unicode-legal output.

    Handles:
    - C + HALANT + V → C + matra
    - Softening (palatalisation / j-glide) via soft_map.json
    """

    out = []
    i = 0

    while i < len(tokens):
        tok = tokens[i]

        # Look for C् + V
        if (
            tok.endswith(HALANT)
            and i + 1 < len(tokens)
            and tokens[i + 1] in VOWEL_TO_MATRA
        ):
            consonant = tok[:-1]
            vowel = tokens[i + 1]
            matra = VOWEL_TO_MATRA[vowel]

            rendered = consonant + matra

            # ---- SOFTENING LOGIC ----
            if latin_tokens is not None:
                latin_vowel = latin_tokens[i + 1]
                latin_cons = latin_tokens[i]

                if (
                    latin_vowel in SOFTENING_VOWELS
                    and latin_cons in _SOFT_MAP.get(latin_vowel, [])
                ):
                    # enforce fronted articulation
                    rendered = rendered + HALANT

            out.append(rendered)
            i += 2
            continue

        # Default: emit token as-is
        out.append(tok)
        i += 1

    return "".join(out)
