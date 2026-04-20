---
name: springer-citation-audit
description: Audits citations and bibliography. Detects orphan bib entries (defined but not cited), dangling cite keys (cited but missing from bib), and citation-formatting issues. Use when the user asks to check citations, bibliography, references, or .bib hygiene.
---

# Citation Audit

## Checks

1. Every `\cite{key}` resolves to an entry in `references.bib`.
2. Every entry in `references.bib` is cited ≥ once (Springer: uncited
   entries must move to Additional Reading or be removed).
3. No spaces after commas inside `\cite{...}` (book-rules.mdc).
4. No mixed citation styles (project uses numeric biblatex; flags
   `\citep`, `\citet`, `\citeauthor`).

## Output

`docs/audit_reports/citations_<timestamp>.md`.
