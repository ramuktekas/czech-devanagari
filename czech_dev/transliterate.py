# czech_dev/transliterate.py

from .preprocess import preprocess
from .schwa import apply_schwa
from .render import render


def transliterate(text: str) -> str:
    latin, dev = preprocess(text)
    dev = apply_schwa(latin, dev)
    return render(dev, latin_tokens=latin)
