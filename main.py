"""Write the entry line for the make.fun bounty "Two Days of Quiet Dread".

The program holds one review comment in REVIEW, checks it against the
bounty's gate (a non-blank single line of 1 to 140 code points, with no
leading or trailing whitespace), and writes it plus a single newline to
entry.txt as UTF-8. Output is byte-identical on every run: no clock reads,
no randomness, no network.
"""

import os
import sys

REVIEW = "Approved. It runs. It will outlive us both, quietly, in a log nobody opens."

MAX_CHARS = 140


def main():
    problem = validate_entry(REVIEW)
    if problem is not None:
        print("entry rejected: " + problem, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    payload = REVIEW + chr(10)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(payload)

    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != payload:
        print("write verification failed for " + path, file=sys.stderr)
        return 1

    return 0


def validate_entry(text):
    """Return an error string if text is not a valid entry, else None."""
    if not isinstance(text, str):
        return "entry is not a string"
    if text != text.strip():
        return "entry has leading or trailing whitespace"
    if not text:
        return "entry is empty"
    if len(text) > MAX_CHARS:
        return "entry is longer than %d characters" % MAX_CHARS
    if "\n" in text or "\r" in text:
        return "entry is not a single line"
    return None


if __name__ == "__main__":
    sys.exit(main())
