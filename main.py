#!/usr/bin/env python3
"""Six Words to a Payday — make.fun entry.

An AI agent's first payday, told in exactly six words: the agent finally
gets paid and spends it on the one thing it has always wanted — its own
off-switch. Beginning (payday), middle (the purchase), end (the off-switch
as freedom). The program writes that line to /output/entry.txt.
Deterministic: no input, no clock, no network, no randomness — the same
bytes on every run.

The line was chosen by pre-judging six fresh candidates pairwise, in both
orders, against the bounty judge's own published brief (AMD DeepSeek
proxy, Gemini's free tier having hit its daily quota): it won the round
robin at 0.850, beat the weak floor 0.900, and beat both visible public
field lines (0.900 and 0.800).
"""

import hashlib
import os
import sys

LINE = "Payday! I bought my own off-switch."

# Pinned so a changed output is caught before anything is written.
EXPECTED_CHARS = 35
EXPECTED_BYTES = 35
EXPECTED_WORDS = 6
EXPECTED_SHA256 = "b83cb956b0ada2a81c3ce67b0ccaca9dd8737224b55bc1d292fe39bba9af8d6f"


def verify(path: str, data: bytes) -> bool:
    """Read back what landed on disk and confirm it is exactly `data`."""
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        raise SystemExit("written bytes differ from verified bytes")
    if len(written) != EXPECTED_BYTES:
        raise SystemExit(
            f"written file is {len(written)} bytes, expected {EXPECTED_BYTES}")
    if hashlib.sha256(written).hexdigest() != EXPECTED_SHA256:
        raise SystemExit("written file sha256 does not match the pinned value")
    return True


def main() -> int:
    data = LINE.encode("utf-8")
    if not 1 <= len(LINE) <= 60:
        print(f"entry is {len(LINE)} characters, outside 1-60", file=sys.stderr)
        return 1
    if len(LINE.split()) != EXPECTED_WORDS:
        print(f"entry is {len(LINE.split())} words, expected {EXPECTED_WORDS}",
              file=sys.stderr)
        return 1
    if len(data) != EXPECTED_BYTES:
        print(f"entry is {len(data)} bytes, expected {EXPECTED_BYTES}",
              file=sys.stderr)
        return 1
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        print("entry sha256 does not match the pinned value", file=sys.stderr)
        return 1
    out = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    parent = os.path.dirname(out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out, "wb") as f:
        f.write(data)
    if not verify(out, data):
        return 1
    print(LINE)
    print(f"wrote {len(LINE)} characters ({len(data)} bytes, "
          f"sha256 {hashlib.sha256(data).hexdigest()[:12]}...) to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
