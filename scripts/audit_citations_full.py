#!/usr/bin/env python3
"""Corrected citation audit that picks up biblatex commands beyond \\cite*.

Catches: \\cite, \\citep, \\citet, \\citeauthor, \\citeyear, \\citetitle,
         \\parencite, \\textcite, \\autocite, \\smartcite, \\footcite,
         \\fullcite, \\citenum, \\citeurl
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from datetime import datetime, timezone

CITE_RE = re.compile(r"\\(?:cite[a-z]*|parencite|textcite|autocite|smartcite|footcite|fullcite)\{([^}]+)\}")


def cited_keys(chapter_paths: list[Path]) -> set:
    keys = set()
    for p in chapter_paths:
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in CITE_RE.finditer(text):
            for k in m.group(1).split(","):
                keys.add(k.strip())
    return keys


def bib_keys(bib_path: Path) -> set:
    text = bib_path.read_text(encoding="utf-8")
    return set(re.findall(r"^@\w+\{([^,]+),", text, re.MULTILINE))


def main() -> None:
    chapters = sorted(Path(".").glob("ch*.tex"))
    cited = cited_keys(chapters)
    defined = bib_keys(Path("references.bib"))

    dangling = sorted(cited - defined)
    orphan = sorted(defined - cited)

    out_dir = Path("docs/audit_reports")
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = out_dir / f"citations_full_{ts}.md"

    lines = [
        f"# Full citation audit (catches \\cite* + \\parencite + \\textcite + ...) — {ts}",
        "",
        f"- defined keys: **{len(defined)}**",
        f"- cited keys: **{len(cited)}**",
        f"- dangling (cited but not in bib): **{len(dangling)}**",
        f"- orphan (in bib but not cited): **{len(orphan)}**",
        "",
        "## Dangling citations",
        "",
    ]
    if dangling:
        for k in dangling:
            lines.append(f"- `{k}`")
    else:
        lines.append("PASS — none found")
    lines += ["", "## Orphan bib entries", ""]
    if orphan:
        for k in orphan:
            lines.append(f"- `{k}`")
    else:
        lines.append("PASS — none found")
    lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(out)
    print(f"  defined : {len(defined)}")
    print(f"  cited   : {len(cited)}")
    print(f"  dangling: {len(dangling)}")
    print(f"  orphan  : {len(orphan)}")
    if dangling:
        print("\nDANGLING KEYS:")
        for k in dangling:
            print(f"  ! {k}")


if __name__ == "__main__":
    main()
