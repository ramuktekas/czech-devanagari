import sys
from .transliterate import transliterate

def main():
    if len(sys.argv) < 2:
        print("Usage: czech2dev 'text'")
        return
    print(transliterate(sys.argv[1]))
