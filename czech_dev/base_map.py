import json
from pathlib import Path

BASE_MAP = json.loads(
    (Path(__file__).parent.parent / "data" / "base_map.json").read_text()
)

def map_base(tokens):
    return [BASE_MAP.get(t, t) for t in tokens]
