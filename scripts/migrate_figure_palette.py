#!/usr/bin/env python3
"""
Migrate per-figure \definecolor declarations to the book palette.

For every \begin{figure} ... \end{figure} block, this script:

  1. Parses \definecolor{<name>}{RGB}{R,G,B} inside the block.
  2. Maps each local color name to the nearest book palette color
     (llmblue, llmorange, llmgreen, llmpurple, llmgray) by Euclidean
     distance in RGB space.
  3. Deletes the \definecolor line.
  4. Replaces every remaining occurrence of the local color name
     inside the figure block with the mapped palette color.

The palette is defined once in macros.tex; this script never redefines it.

Usage:
  python3 scripts/migrate_figure_palette.py [chapter.tex ...]

With no arguments, runs across ch*.tex in repo root.
Idempotent: already-migrated figures are skipped.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PALETTE = {
    "llmblue":   (44, 102, 146),
    "llmorange": (201, 111,  29),
    "llmgreen":  ( 34, 139,  96),
    "llmpurple": (123,  88, 163),
    "llmgray":   ( 90,  90,  90),
}

DEFINECOLOR_RE = re.compile(
    r"^\s*\\definecolor\{([A-Za-z0-9_]+)\}\{RGB\}\{\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\}\s*%?.*$"
)

FIG_BEGIN = "\\begin{figure}"
FIG_END   = "\\end{figure}"


def nearest_palette(rgb: tuple[int, int, int]) -> str:
    def dist(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
        return sum((x - y) ** 2 for x, y in zip(a, b))
    return min(PALETTE, key=lambda name: dist(PALETTE[name], rgb))


def migrate_block(lines: list[str], start: int, end: int) -> int:
    """Mutate lines[start:end+1] in place. Returns number of \definecolor lines removed."""
    # Step 1: collect local color mappings
    mapping: dict[str, str] = {}
    to_delete: list[int] = []
    for i in range(start, end + 1):
        m = DEFINECOLOR_RE.match(lines[i])
        if not m:
            continue
        name, r, g, b = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4))
        # Skip if the name is already a palette name or is the \swatch macro redefinition
        if name in PALETTE:
            continue
        palette_color = nearest_palette((r, g, b))
        mapping[name] = palette_color
        to_delete.append(i)

    if not mapping:
        return 0

    # Step 2: delete \definecolor lines (in reverse order to preserve indices)
    for idx in reversed(to_delete):
        del lines[idx]
    # Adjust end
    end -= len(to_delete)

    # Step 3: replace local color names within the (now-shifted) figure block.
    # Build one compiled regex per local name to match word-boundary usage.
    # We search for the exact color token in LaTeX color-consuming commands and general text.
    # Examples of use sites to catch:
    #   fill=userblue!15
    #   draw=userblue!70
    #   color=userblue!70!black
    #   \color{userblue}
    #   userblue!20
    #
    # Strategy: do a regex replace that matches the local name as a whole word.
    for name, palette in mapping.items():
        rx = re.compile(r"\b" + re.escape(name) + r"\b")
        for i in range(start, end + 1):
            if rx.search(lines[i]):
                lines[i] = rx.sub(palette, lines[i])

    return len(to_delete)


def process_file(path: Path) -> tuple[int, int]:
    src = path.read_text().splitlines(keepends=True)
    n_figs = 0
    n_removed = 0
    i = 0
    while i < len(src):
        if FIG_BEGIN in src[i]:
            j = i + 1
            while j < len(src) and FIG_END not in src[j]:
                j += 1
            if j < len(src):
                removed = migrate_block(src, i, j)
                if removed:
                    n_figs += 1
                    n_removed += removed
                # Adjust end pointer since migrate_block may have shrunk the slice
                # Advance i to the new end (it will move up by `removed`)
                j -= removed
            i = j + 1
        else:
            i += 1
    if n_removed:
        path.write_text("".join(src))
    return n_figs, n_removed


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        files = [Path(a) for a in argv[1:]]
    else:
        files = sorted(Path(".").glob("ch*.tex"))
    total_figs = 0
    total_removed = 0
    for f in files:
        figs, removed = process_file(f)
        if removed:
            print(f"{f}: {figs} figures migrated, {removed} \\definecolor lines removed")
        total_figs += figs
        total_removed += removed
    print(f"Total: {total_figs} figures migrated, {total_removed} \\definecolor lines removed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
