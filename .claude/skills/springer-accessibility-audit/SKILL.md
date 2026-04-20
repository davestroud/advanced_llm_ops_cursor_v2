---
name: springer-accessibility-audit
description: Audits accessibility signals — caption takeaway language, caption length, empty captions, and index density per chapter. Use when the user asks about accessibility, alt text, caption quality, reader takeaway, or index entries.
---

# Accessibility Audit

## Checks

1. Captions starting with passive-contents language (flag for rewrite).
2. Suspiciously short captions (< 20 chars).
3. Empty captions.
4. Index entries (`\index{}`) per chapter; < 10 flagged as thin indexing.

## Output

`docs/audit_reports/accessibility_<timestamp>.md`.
