# czech_dev/schwa.py

import json
from pathlib import Path

from .fronting import remove_fronting
from .base_map import BASE_MAP


# Load cluster rules
_CLUSTER_RULES = json.loads(
    (Path(__file__).parent.parent / "data" / "cluster_map.json").read_text()
)["forbidden_rules"]


LIQUIDS = {"r", "l"}
AFFRICATES = {"c", "č", "dž"}
NASALS = {"m", "n", "ň"}
STOPS = {"p", "b", "t", "d", "k", "g"}
FRICATIVES = {"f", "v", "s", "z", "š", "ž", "h", "ch"}


def _is_affricate(symbol: str) -> bool:
    return symbol in AFFRICATES


def _is_liquid(symbol: str) -> bool:
    return symbol in LIQUIDS


def _is_nasal(symbol: str) -> bool:
    return symbol in NASALS


def _is_stop(symbol: str) -> bool:
    return symbol in STOPS


def _is_fricative(symbol: str) -> bool:
    return symbol in FRICATIVES


def _sonority(symbol: str) -> int:
    """
    Higher number = higher sonority
    """
    if _is_stop(symbol):
        return 1
    if _is_fricative(symbol):
        return 2
    if _is_nasal(symbol):
        return 3
    if _is_liquid(symbol):
        return 4
    return 0


def is_forbidden_cluster(c1: str, c2: str) -> bool:
    """
    Determine whether a Czech consonant cluster C1C2 is forbidden.
    """

    # Both must be consonants
    if c1 not in BASE_MAP["consonants"] or c2 not in BASE_MAP["consonants"]:
        return False

    pair = c1 + c2

    # Rule 1: liquid-liquid
    if pair in _CLUSTER_RULES["liquid_liquid"]:
        return True

    # Rule 2: affricate-initial
    if c1 in AFFRICATES:
        return True

    # Rule 3: ř cannot cluster
    if c1 == "ř":
        return True

    # Rule 4: nasal + stop (unless exception)
    if _is_nasal(c1) and _is_stop(c2):
        if pair not in _CLUSTER_RULES["nasal_stop_exceptions"]:
            return True

    # Rule 5: sonority fall
    if _CLUSTER_RULES.get("sonority_fall", False):
        if _sonority(c1) >= _sonority(c2):
            return True

    return False


def apply_schwa(latin_tokens, dev_tokens):
    """
    Restore schwa (remove halant) on C1 when forbidden C1C2 clusters occur.

    Assumptions:
    - All consonants initially have halant
    - dev_tokens are aligned with latin_tokens
    """

    out = dev_tokens[:]

    for i in range(len(latin_tokens) - 1):
        c1 = latin_tokens[i]
        c2 = latin_tokens[i + 1]

        if is_forbidden_cluster(c1, c2):
            out[i] = remove_fronting(out[i])

    return out
