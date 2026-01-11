import json
from pathlib import Path

FRONTING = json.loads(
    (Path(__file__).parent.parent / "data" / "fronting_map.json").read_text()
)

def apply_fronting(tokens, dev_tokens):
    out = []
    for lat, dev in zip(tokens, dev_tokens):
        if lat in FRONTING:
            out.append(FRONTING[lat])
        else:
            out.append(dev)
    return out
