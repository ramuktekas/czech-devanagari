def parse(text: str) -> list[str]:
    text = text.lower()
    tokens = []
    i = 0

    while i < len(text):
        if text[i:i+2] == "ch":
            tokens.append("ch")
            i += 2
        elif text[i:i+2] == "dž":
            tokens.append("dž")
            i += 2
        else:
            tokens.append(text[i])
            i += 1

    return tokens
