#!/usr/bin/env python3
"""Remove specified entries from references.bib by key.

Safe to re-run: keys not present are silently skipped.
Usage: python3 scripts/bib_delete_keys.py <key1> <key2> ...
       python3 scripts/bib_delete_keys.py --file <keys-file>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def parse_entries(text: str) -> list[tuple[int, int, str | None]]:
    """Returns list of (start_offset, end_offset_inclusive, key_or_None)."""
    entries = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] != "@":
            i += 1
            continue
        m = re.match(r"@(\w+)\{([^,]+),", text[i:])
        if not m:
            i += 1
            continue
        key = m.group(2).strip()
        depth = 0
        j = i
        while j < n:
            c = text[j]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        entries.append((i, j, key))
        i = j + 1
    return entries


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print("usage: bib_delete_keys.py <key1> ... | --file <path>")
        sys.exit(1)
    if args[0] == "--file":
        keys = [k.strip() for k in Path(args[1]).read_text().splitlines() if k.strip() and not k.startswith("#")]
    else:
        keys = args
    keys_set = set(keys)
    bib_path = Path("references.bib")
    text = bib_path.read_text(encoding="utf-8")
    entries = parse_entries(text)

    # build new text by skipping entries with keys in keys_set
    keep_chunks = []
    cursor = 0
    deleted = []
    for start, end, key in entries:
        if key in keys_set:
            keep_chunks.append(text[cursor:start])
            cursor = end + 1
            # also consume trailing whitespace/newlines so we don't leave gaps
            while cursor < len(text) and text[cursor] in " \n\t":
                if text[cursor] == "\n":
                    cursor += 1
                    break
                cursor += 1
            deleted.append(key)
    keep_chunks.append(text[cursor:])
    new_text = "".join(keep_chunks)

    if not deleted:
        print("no entries deleted (none of the requested keys were found)")
        return
    bib_path.write_text(new_text, encoding="utf-8")
    print(f"deleted {len(deleted)} entries:")
    for k in deleted:
        print(f"  - {k}")
    not_found = [k for k in keys if k not in deleted]
    if not_found:
        print(f"\n{len(not_found)} requested keys not found in bib:")
        for k in not_found:
            print(f"  ? {k}")


if __name__ == "__main__":
    main()
