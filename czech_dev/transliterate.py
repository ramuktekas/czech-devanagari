from .parser import parse
from .base_map import map_base
from .fronting import apply_fronting
from .schwa import apply_schwa

def transliterate(text: str) -> str:
    tokens = parse(text)
    dev = map_base(tokens)
    dev = apply_fronting(tokens, dev)
    dev = apply_schwa(tokens, dev)
    return "".join(dev)
