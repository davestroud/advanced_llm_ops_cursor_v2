---
name: springer-cross-ref-audit
description: Audits internal cross-references. Ensures every \ref resolves to a \label and every \label is referenced. Use when the user asks to check cross-references, orphan labels, dangling refs, or internal links.
---

# Cross-Reference Audit

## Checks

1. Every `\ref{X}` has a matching `\label{X}`.
2. Every `\label{X}` is referenced by ≥ 1 `\ref{X}`.
3. No "above/below" replacing explicit references to labeled artifacts.

## Output

`docs/audit_reports/cross_refs_<timestamp>.md`.
