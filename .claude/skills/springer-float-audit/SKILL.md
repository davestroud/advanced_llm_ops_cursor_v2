---
name: springer-float-audit
description: Audits figure, table, and listing placement, captions, labels, widths, and references. Use when the user asks to check figures, tables, listings, float placement, captions, labels, or artifact references. Always use when reviewing visual artifacts for publication readiness.
---

# Springer Float Audit

## Checks

1. **Float specifier** is `[t]` or `[tb]`; `[H]`, `[h]`, `[h!]` flagged.
2. **Label namespace** per artifact type (`fig:chXX_`, `tab:chXX_`, `lst:chXX_`,
   `alg:chXX_`).
3. **Orphan labels** — defined but never referenced.
4. **Dangling references** — `\ref{}` with no `\label{}`.
5. **Weak caption openings** — heuristic flag for "A diagram showing…",
   "Illustration of…", "Example of…" etc.
6. **Per-chapter counts** — figures, tables, listings.

## Output

`docs/audit_reports/floats_<timestamp>.md` with per-chapter counts and
itemized orphan/dangling lists.
