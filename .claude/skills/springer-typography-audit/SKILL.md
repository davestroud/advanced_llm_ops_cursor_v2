---
name: springer-typography-audit
description: Audits font sizes in graphics, artifact widths, sectioning depth, vertical-spacing hacks, and grayscale safety indicators. Use when the user asks to check typography, readability, print-safe colors, section hierarchy, font sizes, or widths in figures.
---

# Typography Audit

## Checks

1. No `\tiny` or `\scriptsize` (book-rules.mdc: min `\footnotesize`).
2. No `\paragraph` or `\subparagraph` (use `\subsubsection`; previously
   fixed across 256+ instances).
3. Widths ≤ 0.95\linewidth (flags 0.96–1.0 and `\textwidth`).
4. No manual vertical-spacing hacks outside tables/TikZ/boxes
   (`\vspace`, `\vfill`, `\smallskip`, `\medskip`, `\bigskip`).
5. Raster graphics flagged (prefer vector per book-rules.mdc).

## Output

`docs/audit_reports/typography_<timestamp>.md`.
