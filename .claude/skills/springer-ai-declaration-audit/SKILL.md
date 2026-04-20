---
name: springer-ai-declaration-audit
description: Audits compliance with Springer Nature's generative-AI policy. Verifies LLM use is declared in acknowledgements and that no generative-AI figures remain. Use when the user asks about AI policy, LLM declaration, generative AI figures, or Springer AI compliance.
---

# Springer AI Policy Audit

Springer Manuscript Guidelines (current edition):

> Use of an LLM should be properly documented in the acknowledgments
> section of the book front matter for monographs.

> We do not accept figures that were created using generative AI.
> Exceptions to this are detailed in the policy.

## Checks

1. `author/acknowledgement.tex` contains an LLM/AI declaration.
2. No raster figures remain in chapter source (`.png`, `.jpg`, `.jpeg`).
3. Files in `images/` are enumerated for manual review.

## Output

`docs/audit_reports/ai_declaration_<timestamp>.md`.

## Manual review required

This skill flags signals. The author decides what was AI-generated,
what wasn't, and how to phrase the declaration. Use this skill to catch
omissions, not to write the declaration.
