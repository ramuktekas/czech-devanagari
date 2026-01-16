# czech_dev/preprocess.py

from .parser import parse
from .base_map import BASE_MAP
from .fronting import apply_fronting


def preprocess(text: str):
    """
    Parse Czech text and convert it to a normalized Devanagari stream where:
    - consonants get halant by default
    - EXCEPT: consonant immediately before word-final 'a'
    """

    latin_tokens = parse(text)
    dev_tokens = []

    # First pass: base-map everything (no halants yet)
    for tok in latin_tokens:
        if tok in BASE_MAP["consonants"]:
            dev_tokens.append(BASE_MAP["consonants"][tok]["dev"])
        elif tok in BASE_MAP["vowels"]:
            dev_tokens.append(BASE_MAP["vowels"][tok]["dev"])
        else:
            dev_tokens.append(tok)

    # Second pass: apply halant to consonants,
    # except before word-final 'a'
    for i, tok in enumerate(latin_tokens):
        if tok in BASE_MAP["consonants"]:
            # Check if this consonant is immediately before word-final 'a'
            is_before_final_a = (
                i + 1 == len(latin_tokens) - 1
                and latin_tokens[i + 1] == "a"
            )

            if not is_before_final_a:
                dev_tokens[i] = apply_fronting(dev_tokens[i])

    return latin_tokens, dev_tokens
