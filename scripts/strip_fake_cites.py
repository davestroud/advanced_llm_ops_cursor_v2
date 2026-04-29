#!/usr/bin/env python3
"""Strip a list of fake bib keys from \\cite-style commands across .tex files.

For each cite command found:
  * remove the listed keys from its key-list
  * if the list is now empty, remove the entire `\\cite{}`-style command (with one
    trailing space if present)
  * if at least one real key remains, keep the command with only real keys

Logs every change to <log_path>.
"""
from __future__ import annotations
import re
import sys
import json
from pathlib import Path

CITE_RE = re.compile(
    r'\\(cite[a-z]*|parencite|textcite|autocite|smartcite|footcite|fullcite)\{([^}]+)\}',
)

def process_file(path: Path, fake_keys: set[str]) -> tuple[int, list[dict]]:
    text = path.read_text()
    actions: list[dict] = []
    new_lines: list[str] = []
    changed = 0
    for lineno, line in enumerate(text.splitlines(keepends=True), 1):
        new_line = line
        offset = 0
        for m in list(CITE_RE.finditer(line)):
            cmd = m.group(1)
            keys = [k.strip() for k in m.group(2).split(',')]
            kept = [k for k in keys if k not in fake_keys]
            removed = [k for k in keys if k in fake_keys]
            if not removed:
                continue
            changed += 1
            start = m.start() + offset
            end = m.end() + offset
            if kept:
                replacement = f"\\{cmd}{{{','.join(kept)}}}"
                actions.append({
                    'file': str(path), 'line': lineno, 'cmd': cmd,
                    'removed': removed, 'kept': kept, 'kind': 'STRIP'
                })
            else:
                replacement = ''
                # Drop a leading non-breaking tie or single space when present; also
                # drop a trailing space if the next char is punctuation.
                if start > 0 and new_line[start - 1] in ('~', ' ') and end <= len(new_line):
                    start -= 1
                actions.append({
                    'file': str(path), 'line': lineno, 'cmd': cmd,
                    'removed': removed, 'kept': [], 'kind': 'EMPTY-REMOVE'
                })
            removed_len = end - start
            new_line = new_line[:start] + replacement + new_line[end:]
            offset += len(replacement) - removed_len
        new_lines.append(new_line)
    new_text = ''.join(new_lines)
    if new_text != text:
        path.write_text(new_text)
    return changed, actions


def main() -> int:
    if len(sys.argv) < 4:
        print("usage: strip_fake_cites.py <log_path> <key1,key2,...> <file1> [file2 ...]")
        return 2
    log_path = Path(sys.argv[1])
    fake_keys = set(sys.argv[2].split(','))
    total = 0
    all_actions: list[dict] = []
    for fp in sys.argv[3:]:
        path = Path(fp)
        if not path.exists():
            print(f"  skip (missing): {fp}")
            continue
        n, acts = process_file(path, fake_keys)
        if n:
            print(f"  {fp}: {n} cite commands updated")
        total += n
        all_actions.extend(acts)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(all_actions, indent=2))
    print(f"Total: {total} cite commands updated. Log -> {log_path}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
