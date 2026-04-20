---
name: springer-structure-audit
description: Audits the book's macro-structure for Springer Nature monograph compliance. Use whenever the user asks to audit the book structure, check parts, chapters, abstracts, front matter, or back matter. Always use when the user mentions "Springer compliance", "submission readiness", or "book audit".
---

# Springer Structure Audit

Audits parts, chapters, front/back matter against Springer's published
monograph requirements. Produces `docs/audit_reports/structure_<timestamp>.md`.

## Checks

1. **Part count** = 4 (matches `book.tex`).
2. **No subparts** — Springer rule: subparts forbidden.
3. **Chapter skeleton:** each chapter has `\chapter{}`, `\label{ch:}`, and
   `\newrefsegment` (for per-chapter bibliography).
4. **Abstracts ≤ 200 words** per chapter (Springer rule).
5. **Front matter files present** (dedication, foreword, preface,
   acknowledgement, acronym, glossary) and non-empty.
6. **LLM declaration** in `author/acknowledgement.tex` — Springer rule:
   "Use of an LLM ... should be properly documented in the acknowledgments
   section of the book front matter for monographs."

## Output

Markdown table: `check | status | location | reference`.

## Script

`scripts/audit.sh` — pure bash, grep/awk only, deterministic.
