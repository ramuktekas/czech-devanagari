import json
from pathlib import Path

CLUSTERS = json.loads(
    (Path(__file__).parent.parent / "data" / "cluster_map.json").read_text()
)["valid"]

def apply_schwa(tokens, dev_tokens):
    out = []
    i = 0

    while i < len(tokens):
        if i+2 < len(tokens):
            c1, c2, v = tokens[i:i+3]
            if c1+c2 in CLUSTERS:
                out.append(dev_tokens[i] + dev_tokens[i+1])
                i += 2
                continue
        out.append(dev_tokens[i])
        i += 1

    return out
